from dataclasses import dataclass
from typing import List

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
