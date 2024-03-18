from abc import ABC, abstractmethod
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
    def add_ingredient(self):
        pass

    @abstractmethod
    def add_drink(self):
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
