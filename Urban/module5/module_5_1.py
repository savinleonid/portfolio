"""Class objects, attributes and methods"""


class House:
    def __init__(self, name: str, number_of_floors: int):  # initialization on create
        # attributes:
        self.name = name
        self.number_of_floors = number_of_floors

    # method:
    def go_to(self, new_floor: int):
        """
        Prints int number of floor to go if exists
        :param new_floor: floor to go
        """
        if 0 < new_floor <= self.number_of_floors:
            print(new_floor)
        else:
            print("No such floor")


# test
my_home = House("My Home", 3)
my_home.go_to(1)
my_home.go_to(3)
my_home.go_to(4)  # not existing
