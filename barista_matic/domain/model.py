from dataclasses import dataclass
from typing import Tuple

from . import exceptions


@dataclass
class Ingredient:
    name: str
    available_quantity: int
    unit_cost: float

    def deallocate_quantity(self, quantity: int):
        self.available_quantity -= quantity

    def get_available_quantity(self) -> int:
        return self.available_quantity

    def can_deallocate_quantity(self, quantity: int) -> bool:
        return self.available_quantity >= quantity

    def get_cost_for_quantity(self, quantity: int) -> float:
        return self.unit_cost * quantity

    def restock_to_quantity(self, quantity):
        self.available_quantity = quantity

    def __hash__(self):
        return hash(self.name)


@dataclass
class DrinkIngredient:
    ingredient: Ingredient
    ingredient_quantity: int

    def can_be_dispensed(self):
        return self.ingredient.can_deallocate_quantity(self.ingredient_quantity)

    def dispense(self):
        self.ingredient.deallocate_quantity(self.ingredient_quantity)

    def get_cost(self) -> float:
        return self.ingredient.get_cost_for_quantity(self.ingredient_quantity)

    def __hash__(self):
        return hash(self.ingredient)


@dataclass
class Drink:
    name: str
    ingredients: Tuple[DrinkIngredient]

    def can_be_dispensed(self):
        return all(ingredient_line.can_be_dispensed() for ingredient_line in self.ingredients)

    def dispense(self):
        if not self.can_be_dispensed():
            raise exceptions.OutOfStock("Drink cannot be dispensed because ingredients aren't sufficient", self)
        for ingredient_line in self.ingredients:
            ingredient_line.dispense()

    def get_cost(self) -> float:
        return sum(ingredient_line.get_cost() for ingredient_line in self.ingredients)

    def __hash__(self):
        return hash(self.name)
