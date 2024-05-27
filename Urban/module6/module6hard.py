import math


class Figure:
    """Base class of figures"""
    sides_count = 0

    def __init__(self, color, *sides):
        self.__sides = []
        self.__color = []
        self.set_color(*color)
        self.filled = False
        self._create_sides(*sides)

    def _create_sides(self, *sides):
        """Check for appropriate side count sets sides"""
        if len(sides) != self.__class__.sides_count:
            self.set_sides(*[1] * self.__class__.sides_count)
        else:
            self.set_sides(*sides)

    def get_color(self):
        """
        Getter of RGB color code of figure
        :return: [int, int, int]
        """
        return self.__color

    def __is_valid_color(self, codes):
        """
        RGB code validation
        :param codes: set[_T], list[_T]
        :return: bool
        :rtype: bool
        """
        # 3 digit and type check
        if not isinstance(codes, tuple or list) or not len(codes) == 3:
            print("[FAIL]: RGB code must contain 3 integer")
            return False
        # only integer check. 'True' values excepts as integer too, so lets get rid of it
        elif not all(isinstance(code, int) for code in codes) or any(isinstance(code, bool) for code in codes):
            print("[FAIL]: Each number must be integer")
            return False
        # range check
        elif not all(0 <= ele < 256 for ele in codes):
            print("[FAIL]: Each number must be in range [0:256]")
            return False
        # if all right:
        else:
            self.filled = True  # set to true if color filled
            return True

    def set_color(self, *codes):
        """Setter of RGb color code of figure"""
        if self.__is_valid_color(codes):  # validation check
            self.__color = list(codes)  # convert to list even if tuple

    def set_sides(self, *sides):
        """Setter for sides of figure"""
        if self.__is_valid_sides(sides):  # validation check
            self.__sides = list(sides)  # convert to list even if tuple

    def get_sides(self):
        """Getter for sides of figure  """
        return self.__sides

    def __is_valid_sides(self, sides):
        """
        Sides validation
        :param sides: tuple[_T]
        :return: bool
        """
        # type check
        if not isinstance(sides, tuple or list):
            print("[FAIL]: Invalid type")
            return False
        # only integer check. 'True' values excepts as integer too, so lets get rid of it
        elif not all(isinstance(side, int) for side in sides) or any(isinstance(side, bool) for side in sides):
            print("[FAIL]: Each side number must be integer")
            return False
        # each class has its own side count, so there's can't be more side than normal, lets handle it
        elif not len(sides) == self.__class__.sides_count or not sides:
            print(f"[FAIL]: Invalid sides count for class {self.__class__.__name__}")
            return False
        # positive number check
        elif not all(side > 0 for side in sides):
            print("[FAIL]: Each side number must be positive")
            return False
        # if all right:
        else:
            return True

    def __len__(self):
        """Overrides magic method len() to return perimeter of figures"""
        return sum(self.__sides)


class Circle(Figure):
    """Circle class inherited from Figure"""
    sides_count = 1  # override

    def __init__(self, color, *sides):
        super().__init__(color, *sides)  # super init of class Figure
        self.__radius = len(self) / (2 * 3.14)  # radius implementation, belongs to class Circle

    def get_square(self):
        """Calculates and returns area of Circle"""
        return self.__radius ** 2 * 3.14


class Triangle(Figure):
    """Triangle class inherited from Figure"""
    sides_count = 3  # override

    def __init__(self, color, *sides):
        super().__init__(color, *sides)  # super init of class Figure
        # inner attributes to calculate area and height
        self.__sides = self.get_sides()
        self.__base = max(self.__sides)  # longest side base
        self.__height = 2 * self.get_square() / self.__base

    def get_square(self):
        s = len(self) / 2  # semi perimeter
        # Heron's formula to get area of triangle with 3 known side
        return math.sqrt(s * (s - self.__sides[0]) * (s - self.__sides[1]) * (s - self.__sides[2]))


class Cube(Figure):
    """Cube class inherited from Figure"""
    sides_count = 12  # override

    def __init__(self, color, *sides):
        super().__init__(color, *sides)  # super init of class Figure

    def _create_sides(self, *sides):  # override method to make side list of 12 equal sides w/ one input
        if len(sides) != 1:
            self.set_sides(*[1] * self.__class__.sides_count)
        else:
            self.set_sides(*[*sides] * self.__class__.sides_count)

    def get_volume(self):
        """Calculates and returns volume of cube"""
        return self.get_sides()[0] ** 3


# color fail handling test -----------------------
print("Color fail handling test -----------------------\n")
circle1 = Circle((200, 200, 100), 10)
circle1.set_color(0, 0, 0)
test = circle1.get_color()
# 3 digit ------
circle1.set_color()
circle1.set_color(1)
circle1.set_color(1, 2)
circle1.set_color(1, 2)
circle1.set_color(1, 2, 3, 4)
# out of range ------
circle1.set_color(-1, 2, 3)
circle1.set_color(1, 256, 257)
# invalid types ------
circle1.set_color(1.1, 2, 3)
circle1.set_color(1, True, 3)
circle1.set_color(1, 2, [3])
circle1.set_color(1, 2, (3,))
assert test == circle1.get_color()
print("Successful")
print()
print("Sides fail handling test ------------------------\n")

# sides fail handling test ------------------------
triangle = Triangle((100, 200, 250), 3, 4, 5)
begin = triangle.get_sides()

# invalid side count
triangle.set_sides()
triangle.set_sides(1)
triangle.set_sides(1, 2)
triangle.set_sides(1, 2, 3, 4)
# positive number test
triangle.set_sides(-1, 2, 3)
triangle.set_sides(-1, -2, -3)
# only integer test
triangle.set_sides(1.1, 2, 3)
triangle.set_sides(1, True, 3)
triangle.set_sides(1, 2, [3])
triangle.set_sides(1, 2, (3,))
last = triangle.get_sides()
assert begin == last
print("Successful")
print()
print("MAIN TEST -------------------------\n")
circle1 = Circle((200, 200, 100), 10)  # (color, sides)
cube1 = Cube((222, 35, 130), 6)

# color change test:
circle1.set_color(55, 66, 77)  # changed
cube1.set_color(300, 70, 15)  # unchanged
print(circle1.get_color())
print(cube1.get_color())

# sides changing test:
cube1.set_sides(5, 3, 12, 4, 5)  # unchanged
circle1.set_sides(15)  # changed
print(cube1.get_sides())
print(circle1.get_sides())

# perimeter test (circle), thus length:
print(len(circle1))

# volume test (cube):
print(cube1.get_volume())
