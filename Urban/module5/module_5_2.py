"""Special classes"""


class House:
    def __init__(self):  # initialisation
        self._number_of_floors = 0

    def set_new_number_of_floors(self, floors: int) -> None:
        """
        Sets new floor number and prints it
        :param floors: int
        """
        self._number_of_floors = floors
        print(self._number_of_floors)
