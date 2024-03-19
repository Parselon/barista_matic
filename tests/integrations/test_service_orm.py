import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    clear_mappers,
    sessionmaker,
)

from barista_matic.adapters import repository
from barista_matic.adapters.orm import (
    metadata,
    start_mappers,
)
from barista_matic.domain import model
from barista_matic.service_layer import services
from tests import helpers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite://")
    metadata.create_all(engine)
    start_mappers()
    yield engine
    clear_mappers()


@pytest.fixture
def session(in_memory_db):
    return sessionmaker(in_memory_db)()


def given_a_baristamatic_with_sqlalchemy_repository(session, ingredients=None, drinks=None):
    db_repository = repository.SQLAlchemyRepository(session)
    if ingredients:
        for ingredient in ingredients:
            db_repository.add_ingredient(ingredient)
    if drinks:
        for drink in drinks:
            db_repository.add_drink(drink)
    return helpers.given_a_baristamatic_service_with_repository(db_repository)


def test_barista_matic_service_get_menu_returns_a_menu_with_drinks(session):
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

    barista_matic = given_a_baristamatic_with_sqlalchemy_repository(
        session,
        drinks=[drink_1, drink_2]
    )

    helpers.then_the_barista_matic_has_the_expected_menu(
        barista_matic,
        services.Menu({"1": drink_2, "2": drink_1})
    )


def test_barista_matic_service_dispense_drink_by_menu_reference(session):
    ingredient_1 = helpers.given_an_ingredient("ingredient 1", quantity=10)

    drink_1 = helpers.given_a_drink_with_ingredients(
        model.DrinkIngredient(ingredient_1, 1),
        name="drink b"
    )

    barista_matic = given_a_baristamatic_with_sqlalchemy_repository(session, drinks=[drink_1])

    helpers.when_the_barista_dispense_a_drink_by_reference(barista_matic, "1")

    helpers.then_the_ingredient_has_the_expected_stock_in_the_db(session, ingredient_1.name, 9)
