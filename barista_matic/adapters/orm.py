from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import (
    registry,
    relationship,
)

from barista_matic.domain import model

mapper_registry = registry()
metadata = mapper_registry.metadata


ingredient_table = Table(
    "ingredient",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("available_quantity", Integer),
    Column("unit_cost", Float),
)


drink_ingredient_table = Table(
    "drink_ingredient",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ingredient_quantity", Integer),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"))
)


drink_drink_ingredient = Table(
    "drink_drink_ingredient",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("drink_ingredient_id", Integer, ForeignKey("drink_ingredient.id")),
    Column("drink_id", Integer, ForeignKey("drink.id"))

)


drink_table = Table(
    "drink",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)


def start_mappers():
    mapper_registry.map_imperatively(
        model.Ingredient,
        ingredient_table
    )
    drink_ingredients_mapper = mapper_registry.map_imperatively(
        model.DrinkIngredient,
        drink_ingredient_table,
        properties={
            "ingredient": relationship(model.Ingredient)
        }
    )
    mapper_registry.map_imperatively(
        model.Drink,
        drink_table,
        properties={
            "ingredients": relationship(
                drink_ingredients_mapper,
                secondary=drink_drink_ingredient,
                collection_class=list
            )
        }
    )
