from dataclasses import dataclass
from typing import Dict, Tuple, Union, Iterable
from operator import attrgetter

from barista_matic.domain import model


def sort_by_attribute(items: Iterable[Union[model.Ingredient, model.Drink]], attribute: str) -> Iterable[Union[model.Ingredient, model.Drink]]:
    """Sort items by the specified attribute

    Args:
        items (Iterable[Union[model.Ingredient, model.Drink]]): Items to order
        attribute (str): Attribute to be sorted

    Returns:
        Iterable[Union[model.Ingredient, model.Drink]]: Sorted items
    """
    return sorted(
        items,
        key=attrgetter(attribute)
    )


class InvalidSelectedDrink(ValueError):
    pass


@dataclass
class Menu:
    """Represents the menu, it will assing a drink reference for the available drinks"""
    menu_items: Dict[str, model.Drink]

    @classmethod
    def from_iterable(cls, drinks: Iterable[model.Drink]) -> "Menu":
        """Create the menu from the drink list. Also will assign automatically a reference.

        Args:
            drinks (Iterable[model.Drink]): List of drinks

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

    def get_drink_by_reference(self, reference: str) -> model.Drink:
        """Get the drink by menu reference

        Args:
            reference (str): A valis menu reference

        Raises:
            InvalidSelectedDrink: If the reference is not valid for the menu

        Returns:
            model.Drink: The drink with the specified reference
        """
        if reference not in self.menu_items:
            raise InvalidSelectedDrink("Drink is")
        return self.menu_items[reference]

    def __iter__(self):
        return iter(self.menu_items.items())


class BaristaMatic:
    """Barista Matic service. Depends on a repository, to get ingredients and drinks"""
    def __init__(self, repository):
        self.repository = repository

    def get_inventory(self) -> Tuple[model.Ingredient]:
        """Get the list of ingredients, sorted by name

        Returns:
            Tuple[model.Ingredient]: The inventory
        """
        return tuple(
            sort_by_attribute(
                self.repository.get_ingredients(),
                "name",
            )
        )

    def get_menu(self) -> Menu:
        """Return the menu based on existing drinks

        Returns:
            Menu: The menu
        """
        sorted_drinks = sort_by_attribute(
            self.repository.get_drinks(),
            "name"
        ) 
        return Menu.from_iterable(sorted_drinks)

    def dispense_drink_by_menu_reference(self, reference: str) -> model.Drink:
        """Dispense the drink by reference. Use the repository for atomicity.

        Args:
            reference (str): Drink reference

        Returns:
            model.Drink: Dispensed drink
        """
        menu = self.get_menu()
        drink_to_dispense = menu.get_drink_by_reference(reference)
        with self.repository:
            drink_to_dispense.dispense()
        return drink_to_dispense

    def restock_ingredient_to_quantity(self, ingredient: model.Ingredient, quantity: int) -> None:
        """Update the stock for specific ingredient.

        Args:
            ingredient (model.Ingredient): Ingredient to be updated
            quantity (int): New stock quantity
        """
        with self.repository:
            ingredient.restock_to_quantity(quantity)

    def restock_all_ingredients_to_quantity(self, quantity: int) -> None:
        """Update the stock for all ingredients in the inventory

        Args:
            quantity (int): New stock
        """
        for ingredient in self.repository.get_ingredients():
            self.restock_ingredient_to_quantity(ingredient, quantity)
