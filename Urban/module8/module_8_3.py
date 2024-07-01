class Car:
    def __init__(self, model, vin, numbers):
        self.model: str = model
        if self.__is_valid_vin(vin):  # vin validation check
            self.__vin: int = vin
        if self.__is_valid_numbers(numbers):  # number validation check
            self.__numbers: str = numbers

    @staticmethod
    def __is_valid_vin(vin_number):
        """Returns True if all fine, else raises custom proper exception."""
        if not isinstance(vin_number, int):  # only 'int' allowed
            raise IncorrectVinNumber("Incorrect type of vin number")
        elif not 1000000 <= vin_number <= 9999999:  # only 7 digit integer
            raise IncorrectVinNumber("Incorrect range for vin number")
        else:
            return True  # all fine

    @staticmethod
    def __is_valid_numbers(numbers):
        """Returns True if all fine, else raises custom proper exception."""
        if not isinstance(numbers, str):  # only 'str' allowed
            raise IncorrectCarNumbers("Incorrect data type for car number")
        elif not len(numbers) == 6:  # only 6 digit
            raise IncorrectCarNumbers("Incorrect length of car number")
        else:
            return True  # all fine


class IncorrectVinNumber(Exception):
    def __init__(self, message):
        self.message = message


class IncorrectCarNumbers(Exception):
    def __init__(self, message):
        self.message = message


# test
try:
    first = Car('Model1', 1000000, 'f123dj')  # all fine
except IncorrectVinNumber as exc:
    print(exc.message)
except IncorrectCarNumbers as exc:
    print(exc.message)
else:
    print(f'{first.model} successfully created')


try:
    second = Car('Model2', 300, 'т001тр')  # wrong vin range
except IncorrectVinNumber as exc:
    print(exc.message)
except IncorrectCarNumbers as exc:
    print(exc.message)
else:
    print(f'{second.model} successfully created')


try:
    third = Car('Model3', 2020202, 'no number')  # wrong length of number
except IncorrectVinNumber as exc:
    print(exc.message)
except IncorrectCarNumbers as exc:
    print(exc.message)
else:
    print(f'{third.model} successfully created')


try:
    first = Car('Model4', 1000000.0, 'f123dj')  # wrong vin type
except IncorrectVinNumber as exc:
    print(exc.message)
except IncorrectCarNumbers as exc:
    print(exc.message)
else:
    print(f'{first.model} successfully created')


try:
    second = Car('Model5', 3030303, 156897)  # wrong number type
except IncorrectVinNumber as exc:
    print(exc.message)
except IncorrectCarNumbers as exc:
    print(exc.message)
else:
    print(f'{second.model} successfully created')