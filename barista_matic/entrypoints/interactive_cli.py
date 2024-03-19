import contextlib
from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict

from barista_matic.domain import exceptions
from barista_matic import settings


class UserExited(Exception):
    pass


class Command(ABC):
    """Command to be executed"""
    @abstractmethod
    def dispatch(self, barista_matic, user_input):
        pass


class ReStock(Command):
    COMMAND_MSG = "Inventory re-stocked"
    TO_QUANTITY = settings.RESTOCK_QUANTITY

    def dispatch(self, barista_service, *args):
        barista_service.restock_all_ingredients_to_quantity(self.TO_QUANTITY)
        print(self.COMMAND_MSG)


class ExitCli(Command):
    def dispatch(self, *args):
        raise UserExited()


class InvalidCommand(Command):
    COMMAND_MSG = "Invalid selection:"

    def dispatch(self, _, user_input):
        print(f"{self.COMMAND_MSG} {user_input}")


class Dispense(Command):
    COMMAND_MSG = "Dispensing:"
    COMMAND_ERROR = "Out of stock:"

    def dispatch(self, barista_service, user_input):
        try:
            dispensed_drink = barista_service.dispense_drink_by_menu_reference(user_input)
            print(f"{self.COMMAND_MSG} {dispensed_drink.name}")
        except exceptions.OutOfStock as err:
            print(f"{self.COMMAND_ERROR} {err.drink.name}")


class PrintInventory(Command):
    COMMAND_MDG = "Inventory:"

    def dispatch(self, barista_service, *args):
        print(self.COMMAND_MDG)
        for item in barista_service.get_inventory():
            print(f"{item.name},{item.get_available_quantity()}")


class PrintMenu(Command):
    COMMAND_MSG = "Menu:"

    def dispatch(self, barista_service, *args):
        print(self.COMMAND_MSG)
        for reference, drink in barista_service.get_menu():
            print(f"{reference},{drink.name},${drink.get_cost():.2f},{str(drink.can_be_dispensed()).lower()}")


command_mapping = defaultdict(
    lambda: InvalidCommand(),
    {
        "r": ReStock(),
        "q": ExitCli(),
        "DISPENSE": Dispense(),
    }
)


class InteractiveCli:
    INPUTS_TO_IGNORE = ("", )

    def __init__(self, barista_service):
        self.barista_service = barista_service

    def get_command_for_user_input(self, user_input, menu) -> Command:
        if menu.has_reference(user_input):
            return command_mapping["DISPENSE"]
        return command_mapping[user_input]

    def print_inventory(self):
        PrintInventory().dispatch(self.barista_service)

    def print_menu(self):
        PrintMenu().dispatch(self.barista_service)

    def get_valid_user_input(self) -> str:
        """Get user input, ignore if it's empty.

        Returns:
            str: User input
        """
        user_input = ""
        while user_input in self.INPUTS_TO_IGNORE:
            user_input = input("").strip().lower()
        return user_input

    def execute(self):
        """Run the interactive cli.
        Prints inventory and menu, wait for user input and run it, until user exited.
        """
        with contextlib.suppress(UserExited):  # On UserExited, loop will break
            while True:
                self.print_inventory()
                self.print_menu()
                user_input = self.get_valid_user_input()
                command = self.get_command_for_user_input(
                    user_input,
                    self.barista_service.get_menu()
                )
                command.dispatch(self.barista_service, user_input)
