"""Create initial data

Revision ID: 93a6f31d62a9
Revises: 863cc33dd118
Create Date: 2024-03-18 21:22:33.491440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from barista_matic.domain import model
from barista_matic.adapters.orm import start_mappers


# revision identifiers, used by Alembic.
revision: str = '93a6f31d62a9'
down_revision: Union[str, None] = '863cc33dd118'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

bind = op.get_bind()
session = sa.orm.Session(bind=bind)


def upgrade() -> None:
    start_mappers()

    cofee = model.Ingredient("Coffee", 10, 0.75)
    decaf_cofee = model.Ingredient("Decaf Coffee", 10, 0.75)
    sugar = model.Ingredient("Sugar", 10, 0.75)
    cream = model.Ingredient("Cream", 10, 0.25)
    steamed_milk = model.Ingredient("Steamed Milk", 10, 0.35)
    foamed_milk = model.Ingredient("Foamed Milk", 10, 0.35)
    espresso = model.Ingredient("Espresso", 10, 1.1)
    cocoa = model.Ingredient("Cocoa", 10, 0.9)
    whipped_cream = model.Ingredient("Whipped Cream", 10, 1)

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

    # Add bulk
    for drink in (drink_coffee, drink_decaf_coffee, drink_caffe_late, drink_caffe_americano, drink_caffe_mocha, drink_cappuccino):
        session.add(drink)
    session.commit()

def downgrade() -> None:
    pass
