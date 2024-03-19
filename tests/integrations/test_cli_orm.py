from barista_matic.adapters.repository import SQLAlchemyRepository
from barista_matic.domain import model
from tests import helpers

EXPECTED_INVENTORY_OUTPUT = """Inventory:
Cocoa,{stock}
Coffee,{stock}
Cream,{stock}
Decaf Coffee,{stock}
Espresso,{stock}
Foamed Milk,{stock}
Steamed Milk,{stock}
Sugar,{stock}
Whipped Cream,{stock}
"""

EXPECTED_MENU_OUTPUT = """Menu:
1,Caffe Americano,$3.30,true
2,Caffe Latte,$2.55,true
3,Caffe Mocha,$3.35,true
4,Cappuccino,$2.90,true
5,Coffee,$3.25,true
6,Decaf Coffee,$3.25,true
"""


def given_a_repository_with_examples_drink(repository, stock=10):
    cofee = model.Ingredient("Coffee", stock, 0.75)
    decaf_cofee = model.Ingredient("Decaf Coffee", stock, 0.75)
    sugar = model.Ingredient("Sugar", stock, 0.75)
    cream = model.Ingredient("Cream", stock, 0.25)
    steamed_milk = model.Ingredient("Steamed Milk", stock, 0.35)
    foamed_milk = model.Ingredient("Foamed Milk", stock, 0.35)
    espresso = model.Ingredient("Espresso", stock, 1.1)
    cocoa = model.Ingredient("Cocoa", stock, 0.9)
    whipped_cream = model.Ingredient("Whipped Cream", stock, 1)

    drink_coffee = model.Drink(
        "Coffee", [
            model.DrinkIngredient(cofee, 3),
            model.DrinkIngredient(sugar, 1),
            model.DrinkIngredient(cream, 1),
        ]
    )
    drink_decaf_coffee = model.Drink(
        "Decaf Coffee", [
            model.DrinkIngredient(decaf_cofee, 3),
            model.DrinkIngredient(sugar, 1),
            model.DrinkIngredient(cream, 1),
        ]
    )
    drink_caffe_late = model.Drink(
        "Caffe Latte", [
            model.DrinkIngredient(espresso, 2),
            model.DrinkIngredient(steamed_milk, 1),
        ]
    )
    drink_caffe_americano = model.Drink(
        "Caffe Americano", [
            model.DrinkIngredient(espresso, 3),
        ]
    )
    drink_caffe_mocha = model.Drink(
        "Caffe Mocha", [
            model.DrinkIngredient(espresso, 1),
            model.DrinkIngredient(cocoa, 1),
            model.DrinkIngredient(steamed_milk, 1),
            model.DrinkIngredient(whipped_cream, 1),
        ]
    )
    drink_cappuccino = model.Drink(
        "Cappuccino", [
            model.DrinkIngredient(espresso, 2),
            model.DrinkIngredient(steamed_milk, 1),
            model.DrinkIngredient(foamed_milk, 1),
        ]
    )

    with repository as repo:
        repo.add_drink(drink_coffee)
        repo.add_drink(drink_decaf_coffee)
        repo.add_drink(drink_caffe_late)
        repo.add_drink(drink_caffe_americano)
        repo.add_drink(drink_caffe_mocha)
        repo.add_drink(drink_cappuccino)


def then_all_ingredients_in_inventory_has_the_stock(expected_quantity, session):
    all(
        ingredient.available_quantity == expected_quantity
        for ingredient
        in session.query(model.Ingredient).all()
    )


def test_use_cases_restock(session, capsys, monkeypatch):
    repository = SQLAlchemyRepository(session)
    given_a_repository_with_examples_drink(repository, stock=9)

    barista_matic = helpers.given_a_baristamatic_service_with_repository(repository)
    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, ["r", "q"], monkeypatch)

    expected_old_inventory = EXPECTED_INVENTORY_OUTPUT.format(stock=9)
    expected_new_inventory = EXPECTED_INVENTORY_OUTPUT.format(stock=10)

    program_output = capsys.readouterr().out

    assert "Inventory re-stocked" in program_output
    assert expected_old_inventory in program_output
    assert expected_new_inventory in program_output

    then_all_ingredients_in_inventory_has_the_stock(10, session)


def test_use_cases_dispense_the_menu_option_2(session, capsys, monkeypatch):
    repository = SQLAlchemyRepository(session)
    given_a_repository_with_examples_drink(repository, stock=10)

    barista_matic = helpers.given_a_baristamatic_service_with_repository(repository)
    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, ["2", "q"], monkeypatch)

    program_output = capsys.readouterr().out

    assert EXPECTED_MENU_OUTPUT in program_output
    assert "Dispensing: Caffe Latte" in program_output
    assert "Espresso,8" in program_output
    assert "Steamed Milk,9" in program_output

    helpers.then_the_ingredient_has_the_expected_stock_in_the_db(session, "Espresso", 8)
    helpers.then_the_ingredient_has_the_expected_stock_in_the_db(session, "Steamed Milk", 9)
