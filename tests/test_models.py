from typing import Iterable

import pytest

from barista_matic.domain import model
from barista_matic.domain import exceptions


def given_an_ingredient(name="an ingredient", quantity=10, unit_cost=1):
    return model.Ingredient(name, quantity, unit_cost)


def given_a_drink_with_ingredients(*ingredients: Iterable[model.DrinkIngredient], name="a drink"):
    return model.Drink(name, set(ingredients))


def when_the_drink_is_dispensed(a_drink: model.Drink):
    a_drink.dispense()


def then_the_ingredient_has_the_expected_quantity(an_ingredient, expected_quantity):
    assert an_ingredient.get_available_quantity() == expected_quantity, f"The ingredient {an_ingredient} has not the expected quantity {expected_quantity}"


def then_the_drink_has_the_expected_cost(a_drink, expected_cost):
    assert a_drink.get_cost() == expected_cost, f"The drink {a_drink} has not the expectedcost {expected_cost}"


def test_dispense_a_drink_updates_the_inventory():
    an_ingredient = given_an_ingredient(quantity=10)
    a_drink = given_a_drink_with_ingredients(
        model.DrinkIngredient(an_ingredient, 2)
    )

    when_the_drink_is_dispensed(a_drink)

    then_the_ingredient_has_the_expected_quantity(an_ingredient, 8)


def test_dispense_a_drink_with_multiple_ingredients_updates_inventory():
    ingredient_1 = given_an_ingredient(quantity=10)
    ingredient_2 = given_an_ingredient(quantity=9)
    ingredient_3 = given_an_ingredient(quantity=8)

    a_drink = given_a_drink_with_ingredients(
        model.DrinkIngredient(ingredient_1, 1),
        model.DrinkIngredient(ingredient_2, 2),
        model.DrinkIngredient(ingredient_3, 3)
    )

    when_the_drink_is_dispensed(a_drink)

    then_the_ingredient_has_the_expected_quantity(ingredient_1, 9)
    then_the_ingredient_has_the_expected_quantity(ingredient_2, 7)
    then_the_ingredient_has_the_expected_quantity(ingredient_3, 5)


def test_dispense_a_drink_raise_outofstock_if_ingredient_is_not_enough():
    an_ingredient = given_an_ingredient(quantity=1)
    a_drink = given_a_drink_with_ingredients(
        model.DrinkIngredient(an_ingredient, 2)
    )

    with pytest.raises(exceptions.OutOfStock):
        when_the_drink_is_dispensed(a_drink)


def test_dispense_a_drink_with_multiple_ingredients_raise_outofstock_if_at_least_one_ingredient_is_not_enough():
    ingredient_without_stock = given_an_ingredient(quantity=0)
    ingredient_2 = given_an_ingredient(quantity=10)
    ingredient_3 = given_an_ingredient(quantity=10)

    a_drink = given_a_drink_with_ingredients(
        model.DrinkIngredient(ingredient_without_stock, 1),
        model.DrinkIngredient(ingredient_2, 2),
        model.DrinkIngredient(ingredient_3, 3),
    )

    with pytest.raises(exceptions.OutOfStock):
        when_the_drink_is_dispensed(a_drink)


def test_get_cost_of_a_drink_with_multiple_ingredients_computes_expected_cost():
    ingredient_1 = given_an_ingredient(unit_cost=4.4)
    ingredient_2 = given_an_ingredient(unit_cost=5.5)
    ingredient_3 = given_an_ingredient(unit_cost=7.7)

    a_drink = given_a_drink_with_ingredients(
        model.DrinkIngredient(ingredient_1, 1),
        model.DrinkIngredient(ingredient_2, 2),
        model.DrinkIngredient(ingredient_3, 3),
    )

    then_the_drink_has_the_expected_cost(a_drink, 4.4 + 5.5 * 2 + 7.7 * 3)


def test_ingredients_restock():
    an_ingredient = given_an_ingredient(quantity=6)

    an_ingredient.restock_to_quantity(20)

    then_the_ingredient_has_the_expected_quantity(an_ingredient, 20)
