from typing import Iterable
from barista_matic.domain import model
from barista_matic.service_layer import services


def given_an_ingredient(name="an ingredient", quantity=10, unit_cost=1) -> model.Ingredient:
    return model.Ingredient(name, quantity, unit_cost)


def given_a_drink_with_ingredients(*ingredients: Iterable[model.DrinkIngredient], name="a drink") -> model.Drink:
    return model.Drink(name, list(ingredients))


def given_a_baristamatic_service_with_repository(repository) -> services.BaristaMatic:
    return services.BaristaMatic(repository)


def when_the_barista_dispense_a_drink_by_reference(barista_matic, drink_reference):
    return barista_matic.dispense_drink_by_menu_reference(drink_reference)


def then_the_baristamatic_returns_the_ingredients(barista_matic, expected_ingredients):
    assert barista_matic.get_inventory() == expected_ingredients


def then_the_barista_matic_has_the_expected_menu(barista_matic, expected_menu):
    assert barista_matic.get_menu() == expected_menu


def then_the_ingredient_has_the_expected_stock_in_the_db(session, ingredient_name, expected_quantity):
    ingredient = session.query(model.Ingredient).filter(model.Ingredient.name == ingredient_name).all()
    assert ingredient
    assert ingredient[0].get_available_quantity() == expected_quantity
