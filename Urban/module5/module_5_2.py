"""Special classes"""


class House:
    def __init__(self):  # initialisation
        self.number_of_floors = 0

    def set_new_number_of_floors(self, floors: int):
        """
        Sets new floor number and prints it
        :param floors: int
        """
        self.number_of_floors = floors
        print(self.number_of_floors)
