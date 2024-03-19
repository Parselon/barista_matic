from dataclasses import dataclass
from typing import (
    Dict,
    Iterable,
    List,
)

from . import exceptions


@dataclass
class Ingredient:
    """Represents an inventory item"""
    name: str
    available_quantity: int
    unit_cost: float

    def deallocate_quantity(self, quantity: int) -> None:
        """Subtract the quantity used from the stock

        Args:
            quantity (int): Quantity to substract
        """
        self.available_quantity -= quantity

    def get_available_quantity(self) -> int:
        """Returns the available quantity

        Returns:
            int: Available quantity
        """
        return self.available_quantity

    def can_deallocate_quantity(self, quantity: int) -> bool:
        """Check if there is sufficient stock to use the specified quantity

        Args:
            quantity (int): Quantity to use

        Returns:
            bool: Is stock quantity enough
        """
        return self.available_quantity >= quantity

    def get_cost_for_quantity(self, quantity: int) -> float:
        """Compute the cost for using the specified quantity

        Args:
            quantity (int): Quantity to get the cost

        Returns:
            float: Total cost
        """
        return self.unit_cost * quantity

    def restock_to_quantity(self, quantity: int) -> None:
        """Update the stock to the specified quantity

        Args:
            quantity (int): New quantity stock
        """
        self.available_quantity = quantity

    def __hash__(self):
        return hash(self.name)


@dataclass
class DrinkIngredient:
    """Represent the ingredient used for a specific drink"""
    ingredient: Ingredient
    ingredient_quantity: int

    def can_be_dispensed(self) -> bool:
        """Check if the stock of the ingredient is enough to dispense this ingredient

        Returns:
            bool: Can be dispensed
        """
        return self.ingredient.can_deallocate_quantity(self.ingredient_quantity)

    def dispense(self) -> None:
        """Update ingredient stock"""
        self.ingredient.deallocate_quantity(self.ingredient_quantity)

    def get_cost(self) -> float:
        """Get cost for using this component

        Returns:
            float: [description]
        """
        return self.ingredient.get_cost_for_quantity(self.ingredient_quantity)

    def __hash__(self):
        return hash(self.ingredient)


@dataclass
class Drink:
    """Represents a drink with their ingredients"""
    name: str
    ingredients: List[DrinkIngredient]

    def can_be_dispensed(self) -> bool:
        """Check if the stock of every ingredient to use is enough

        Returns:
            bool: Stock is enough
        """
        return all(ingredient_line.can_be_dispensed() for ingredient_line in self.ingredients)

    def dispense(self) -> None:
        """Dispense the drink and update the stock for every ingredient.

        Raises:
            exceptions.OutOfStock: Ingredient stock is not enough
        """
        if not self.can_be_dispensed():
            raise exceptions.OutOfStock("Drink cannot be dispensed because ingredients aren't sufficient", self)
        for ingredient_line in self.ingredients:
            ingredient_line.dispense()

    def get_cost(self) -> float:
        """Campute cost for every ingredient used in the drink

        Returns:
            float: Drink cost
        """
        return sum(ingredient_line.get_cost() for ingredient_line in self.ingredients)

    def __hash__(self):
        return hash(self.name)


@dataclass
class Menu:
    """Represents the menu, it will assing a drink reference for the available drinks"""
    menu_items: Dict[str, Drink]

    @classmethod
    def from_iterable(cls, drinks: Iterable[Drink]) -> "Menu":
        """Create the menu from the drink list. Also will assign automatically a reference.

        Args:
            drinks (Iterable[Drink]): List of drinks

        Returns:
            [Menu]: A menu for the specified drinks
        """
        return cls(
            {str(reference): drink for reference, drink in enumerate(drinks, start=1)}
        )

    def has_reference(self, reference: str) -> bool:
        """Check if the reference exists in the menu

        Args:
            reference (str): The drink reference

        Returns:
            bool: Exists in the menu?
        """
        return reference in self.menu_items

    def get_drink_by_reference(self, reference: str) -> Drink:
        """Get the drink by menu reference

        Args:
            reference (str): A valis menu reference

        Raises:
            InvalidSelectedDrink: If the reference is not valid for the menu

        Returns:
            model.Drink: The drink with the specified reference
        """
        if reference not in self.menu_items:
            raise exceptions.InvalidSelectedDrink("Drink is")
        return self.menu_items[reference]

    def __iter__(self):
        return iter(self.menu_items.items())
