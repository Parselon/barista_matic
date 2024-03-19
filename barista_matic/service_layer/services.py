from operator import attrgetter
from typing import (
    Iterable,
    Tuple,
    Union,
)

from barista_matic.adapters import repository
from barista_matic.domain import model


def sort_by_attribute(
    items: Iterable[Union[model.Ingredient, model.Drink]], attribute: str
) -> Iterable[Union[model.Ingredient, model.Drink]]:
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


class BaristaMatic:
    """Barista Matic service. Depends on a repository, to get ingredients and drinks"""
    def __init__(self, repository: repository.AbstractRepository):
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

    def get_menu(self) -> model.Menu:
        """Return the menu based on existing drinks

        Returns:
            model.Menu: The menu
        """
        sorted_drinks = sort_by_attribute(
            self.repository.get_drinks(),
            "name"
        )
        return model.Menu.from_iterable(sorted_drinks)

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
