"""Overriding decorator"""


class Building:
    def __init__(self, number_of_floors: int, building_type: str):
        self.number_of_floors = number_of_floors
        self.building_type = building_type

    def __eq__(self, other):
        if isinstance(other, Building):  # make sure 'other' is from 'Building' class
            return self.number_of_floors == other.number_of_floors and self.building_type == other.building_type


# test
b1 = Building(30, "Hotel")
b2 = Building(5, "Apartment")
b3 = Building(5, "Apartment")

print("Is same?:", b1 == b2)  # different
print("Is same?:", b2 == b3)  # same

