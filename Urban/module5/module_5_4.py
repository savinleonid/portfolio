"""Class variable test"""


class Building:
    total = 0  # class variable shared by all instances

    def __init__(self):
        Building.total += 1  # will increment class variable on each new instance created


# test: By creating 40 new instances of class Building, shared variable 'total' should be equal to 40 too
buildings = []
for _ in range(40):
    buildings.append(Building())

print(Building.total)
