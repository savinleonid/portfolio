"""Overriding class methods and attributes"""


class Car:  # base class
    price = 1000000  # base attribute

    def __init__(self):
        self.horse_power = 0

    # base method
    def horse_powers(self):
        return self.horse_power


class Nissan(Car):
    price = 800000  # base attribute overridden

    def horse_powers(self):  # base method overridden
        self.horse_power = 200
        return self.horse_power


class Kia(Car):
    price = 700000  # base attribute overridden

    def horse_powers(self):  # base method overridden
        self.horse_power = 150
        return self.horse_power


# test
n = Nissan()
k = Kia()

print(n.price, n.horse_powers())  # Nissan
print(k.price, k.horse_powers())  # Kia
