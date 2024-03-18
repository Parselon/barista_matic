from typing import Iterable
from barista_matic.domain import model


def given_an_ingredient(name="an ingredient", quantity=10, unit_cost=1) -> model.Ingredient:
    return model.Ingredient(name, quantity, unit_cost)


def given_a_drink_with_ingredients(*ingredients: Iterable[model.DrinkIngredient], name="a drink") -> model.Drink:
    return model.Drink(name, list(ingredients))
