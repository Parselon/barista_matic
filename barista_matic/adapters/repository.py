from abc import (
    ABC,
    abstractmethod,
)
from typing import Set

from barista_matic.domain import model


class AbstractRepository(ABC):
    @abstractmethod
    def get_ingredients(self) -> Set[model.Ingredient]:
        pass

    @abstractmethod
    def get_drinks(self) -> Set[model.Drink]:
        pass

    @abstractmethod
    def add_ingredient(self, ingredient: model.Ingredient):
        pass

    @abstractmethod
    def add_drink(self, drink: model.Drink):
        pass

    @abstractmethod
    def commit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.commit()  # Add rollback on error


class FakeRepository(AbstractRepository):
    def __init__(self):
        self.ingredients = set()
        self.drinks = set()

    def add_ingredient(self, ingredient: model.Ingredient):
        self.ingredients.add(ingredient)

    def add_drink(self, drink: model.Drink):
        self.drinks.add(drink)
        for drink_ingredient in drink.ingredients:
            self.add_ingredient(drink_ingredient.ingredient)

    def get_ingredients(self) -> Set[model.Ingredient]:
        return self.ingredients

    def get_drinks(self) -> Set[model.Drink]:
        return self.drinks

    def commit(self):
        pass


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add_ingredient(self, ingredient: model.Ingredient):
        self.session.add(ingredient)
        self.session.commit()

    def add_drink(self, drink: model.Drink):
        self.session.add(drink)
        self.session.commit()

    def get_ingredients(self) -> Set[model.Ingredient]:
        return self.session.query(model.Ingredient).all()

    def get_drinks(self) -> Set[model.Drink]:
        return self.session.query(model.Drink).all()

    def commit(self):
        self.session.commit()
