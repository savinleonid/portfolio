"""Multiple Inheritance and overriding of methods and attributes"""


# Base vehicle constructor
class Vehicle:
    def __init__(self, vehicle_type=None):
        self.vehicle_type = vehicle_type


# Base Car class. Defines minimum attributes for basic car and minimum price
class Car:
    def __init__(self):
        self.price = 1000000
        self.horse_power = 200

    def horse_powers(self):
        return self.horse_power


# inherited class from Car and Vehicle.
# this car is 1000000 more expensive and 150 hp powerful than basic car
# set as Hatchback type
class Nissan(Car, Vehicle):
    def __init__(self):
        # initialize parent classes relatively
        super().__init__()  # first init for Car class
        Vehicle.__init__(self, "Hatchback")  # second init for Vehicle class
        self.price += 1000000  # adds value to parents Car class init value

    # override methode of Car class and adds value
    def horse_powers(self):
        return self.horse_power + 150


# test
v = Vehicle()
c = Car()
n = Nissan()
print(f"Vehicle Type: {v.vehicle_type}, Price: {c.price}, Horse Power: {c.horse_powers()}")
print(f"Vehicle Type: {n.vehicle_type}, Price: {n.price}, Horse Power: {n.horse_powers()}")
