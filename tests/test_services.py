import pytest

from barista_matic.adapters.repository import FakeRepository
from barista_matic.domain import (
    exceptions,
    model,
)
from barista_matic.service_layer import services
from tests import helpers


def given_a_baristamatic_with_fake_repository(ingredients=None, drinks=None):
    repository = FakeRepository()
    if ingredients:
        for ingredient in ingredients:
            repository.add_ingredient(ingredient)
    if drinks:
        for drink in drinks:
            repository.add_drink(drink)
    return helpers.given_a_baristamatic_service_with_repository(repository)




def then_the_ingredient_has_the_expected_stock(ingredient, expected_stock):
    assert ingredient.get_available_quantity() == expected_stock


def test_barista_get_inventory_on_empty_repository():
    barista_matic = given_a_baristamatic_with_fake_repository()

    helpers.then_the_baristamatic_returns_the_ingredients(barista_matic, tuple())


def test_barista_matic_service_get_inventory_returns_ordered_ingredients():
    ingredient_2 = helpers.given_an_ingredient("ingredient 2")
    ingredient_1 = helpers.given_an_ingredient("ingredient 1")
    barista_matic = given_a_baristamatic_with_fake_repository(
        ingredients=[ingredient_2, ingredient_1]
    )

    helpers.then_the_baristamatic_returns_the_ingredients(barista_matic, (ingredient_1, ingredient_2))


def test_barista_get_menu_on_empty_repository():
    barista_matic = given_a_baristamatic_with_fake_repository()

    helpers.then_the_barista_matic_has_the_expected_menu(barista_matic, services.Menu({}))


def test_barista_matic_service_get_menu_returns_a_menu_with_drinks():
    ingredient_1 = helpers.given_an_ingredient("ingredient 1")
    ingredient_2 = helpers.given_an_ingredient("ingredient 2")

    drink_1 = helpers.given_a_drink_with_ingredients(
        model.DrinkIngredient(ingredient_1, 1),
        model.DrinkIngredient(ingredient_2, 2),
        name="drink b"
    )
    drink_2 = helpers.given_a_drink_with_ingredients(
        model.DrinkIngredient(ingredient_1, 5),
        name="drink a"
    )

    barista_matic = given_a_baristamatic_with_fake_repository(
        drinks=[drink_1, drink_2]
    )

    helpers.then_the_barista_matic_has_the_expected_menu(
        barista_matic,
        services.Menu({"1": drink_2, "2": drink_1})
    ) 


def test_barista_matic_service_dispense_drink_by_menu_reference():
    class FakeDrink(model.Drink): 
        dispensed : bool = False

        def dispense(self):
            self.dispensed = True

        def assert_was_dispensed(self):
            assert self.dispensed is True, "The drink was not dispensed"

    fake_drink = FakeDrink(name="", ingredients=set())
    barista_matic = given_a_baristamatic_with_fake_repository(drinks=[fake_drink])

    dispensed_drink = helpers.when_the_barista_dispense_a_drink_by_reference(barista_matic, "1")

    fake_drink.assert_was_dispensed()
    assert dispensed_drink is fake_drink


def test_barista_matic_error_when_drink_not_exists_by_reference():
    barista_matic = given_a_baristamatic_with_fake_repository()

    with pytest.raises(services.InvalidSelectedDrink):
        helpers.when_the_barista_dispense_a_drink_by_reference(barista_matic, "1")


def test_barista_matic_get_out_of_stock_error_when_dispensing_a_drink_without_stock():
    an_ingredient = helpers.given_an_ingredient(quantity=1)
    a_drink = helpers.given_a_drink_with_ingredients(
        model.DrinkIngredient(an_ingredient, 2)
    )

    barista_matic = given_a_baristamatic_with_fake_repository(ingredients=[an_ingredient], drinks=[a_drink])

    with pytest.raises(exceptions.OutOfStock) as excinfo:
        helpers.when_the_barista_dispense_a_drink_by_reference(barista_matic, "1")
    assert excinfo.value.drink is a_drink


def test_barista_matic_restock_specific_ingredient():
    NEW_STOCK = 5
    an_ingredient = helpers.given_an_ingredient(quantity=1)

    barista_matic = given_a_baristamatic_with_fake_repository(ingredients=[an_ingredient])

    barista_matic.restock_ingredient_to_quantity(an_ingredient, NEW_STOCK)

    then_the_ingredient_has_the_expected_stock(an_ingredient, NEW_STOCK)


def test_barista_matic_restock_all_ingredients():
    NEW_STOCK = 10
    ingredient_1 = helpers.given_an_ingredient(quantity=1)
    ingredient_2 = helpers.given_an_ingredient(quantity=2)
    ingredient_3 = helpers.given_an_ingredient(quantity=3)

    barista_matic = given_a_baristamatic_with_fake_repository(
        ingredients=[ingredient_1, ingredient_2, ingredient_3]
    )

    barista_matic.restock_all_ingredients_to_quantity(10)

    then_the_ingredient_has_the_expected_stock(ingredient_1, NEW_STOCK)
    then_the_ingredient_has_the_expected_stock(ingredient_2, NEW_STOCK)
    then_the_ingredient_has_the_expected_stock(ingredient_3, NEW_STOCK)
