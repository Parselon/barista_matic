from unittest import mock

import pytest

from barista_matic.domain import (
    exceptions,
    model,
)
from barista_matic.service_layer.services import Menu
from tests import helpers


def given_a_mocked_baristamatic_service(inventory=None, menu=None):
    barista_matic = mock.Mock()
    barista_matic.get_inventory.return_value = inventory or set()
    barista_matic.get_menu.return_value = menu or Menu({})
    return barista_matic


@pytest.mark.timeout(0.1)
def test_cli_quits_on_input_q(monkeypatch, capsys):
    barista_matic = given_a_mocked_baristamatic_service()
    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, ["q"], monkeypatch)

    barista_matic.get_inventory.assert_called_once()
    barista_matic.get_menu.assert_called()

    helpers.then_the_cli_output_has(capsys, "Inventory:\nMenu:\nq\n")


@pytest.mark.timeout(0.1)
def test_cli_prints_inventory_in_the_expected_format(monkeypatch, capsys):
    an_ingredient = model.Ingredient("an ingredient", 2, 1.2)
    barista_matic = given_a_mocked_baristamatic_service({an_ingredient})

    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)
    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, ["Q"], monkeypatch)

    helpers.then_the_cli_output_has(capsys, "Inventory:\nan ingredient,2\n")


@pytest.mark.timeout(0.1)
def test_cli_prints_menu_in_the_expected_format(monkeypatch, capsys):
    drink = model.Drink(
        "a drink",
        (model.DrinkIngredient(model.Ingredient("", 1, 5), 3), )
    )
    barista_matic = given_a_mocked_baristamatic_service(menu=Menu({"1": drink}))

    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, ["Q"], monkeypatch)

    helpers.then_the_cli_output_has(capsys, "Menu:\n1,a drink,$15.00,false\n")


@pytest.mark.timeout(0.1)
def test_cli_prints_invalid_selection(monkeypatch, capsys):
    barista_matic = given_a_mocked_baristamatic_service()

    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, ["i", "q"], monkeypatch)

    helpers.then_the_cli_output_has(capsys, "Invalid selection: i\n")


@pytest.mark.timeout(0.1)
def test_cli_ignores_empty_input(monkeypatch, capsys):
    barista_matic = given_a_mocked_baristamatic_service()

    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, ["", "q"], monkeypatch)

    helpers.then_the_cli_output_has(capsys, "\n\n")


@pytest.mark.timeout(1.0)
def test_cli_dispense_drink_prints_dispensed(monkeypatch, capsys):
    DRINK_REFERENCE = "1"
    drink = model.Drink(
        "a drink",
        (model.DrinkIngredient(model.Ingredient("", 3, 5.0), 3), )
    )
    barista_matic = given_a_mocked_baristamatic_service(menu=Menu({DRINK_REFERENCE: drink}))
    barista_matic.dispense_drink_by_menu_reference.return_value = drink

    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, [DRINK_REFERENCE, "q"], monkeypatch)

    barista_matic.dispense_drink_by_menu_reference.assert_called_once_with(DRINK_REFERENCE)
    helpers.then_the_cli_output_has(capsys, "Dispensing: a drink")


@pytest.mark.timeout(1.0)
def test_cli_dispense_drink_prints_out_of_stock(monkeypatch, capsys):
    DRINK_REFERENCE = "1"

    drink = model.Drink(
        "a drink",
        (model.DrinkIngredient(model.Ingredient("", 1, 5.0), 3), )
    )

    barista_matic = given_a_mocked_baristamatic_service(menu=Menu({"1": drink}))
    barista_matic.dispense_drink_by_menu_reference.side_effect = exceptions.OutOfStock("", drink=drink)

    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, [DRINK_REFERENCE, "q"], monkeypatch)

    barista_matic.dispense_drink_by_menu_reference.assert_called_once_with(DRINK_REFERENCE)
    helpers.then_the_cli_output_has(capsys, "Out of stock: a drink\n")


@pytest.mark.timeout(1.0)
def test_cli_restocking(monkeypatch, capsys):
    barista_matic = given_a_mocked_baristamatic_service()

    cli = helpers.given_an_interactive_cli_for_barista_service(barista_matic)

    helpers.when_the_interactive_cli_runs_with_user_inputs(cli, ["r", "q"], monkeypatch)

    barista_matic.restock_all_ingredients_to_quantity.assert_called_once_with(10)
    helpers.then_the_cli_output_has(capsys, "Inventory re-stocked\n")
