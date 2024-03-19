class OutOfStock(ValueError):
    """The ingredient is out of stock"""
    def __init__(self, value, drink):
        super().__init__(value)
        self.drink = drink


class DrinkNotExist(ValueError):
    """Drink doesn't exists"""


class InvalidSelectedDrink(ValueError):
    """The selection is invalid"""
