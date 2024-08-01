class Vehicle:
    __COLOR_VARIANTS = ['blue', 'red', 'green', 'black', 'white']

    def __init__(self, owner, model, color, engine_power):
        self.owner = owner
        self.__model: str = model
        self. __engine_power: int = engine_power
        self. __color: str = color

    def get_model(self):
        return f"Model: {self.__model}"

    def get_horsepower(self):
        return f"Engine power: {self.__engine_power}"

    def get_color(self):
        return f"Color: {self.__color}"

    def print_info(self):
        print(self.get_model())
        print(self.get_horsepower())
        print(self.get_color())
        print("Owner:", self.owner)

    def set_color(self, new_color: str):
        if new_color.lower() in self.__COLOR_VARIANTS:
            self.__color = new_color
        else:
            print("Can not change color to", new_color)


class Sedan(Vehicle):
    __PASSENGERS_LIMIT = 5

    def __init__(self, owner, model, color, engine_power):
        super().__init__(owner, model, color, engine_power)


# test
# Current colors __COLOR_VARIANTS = ['blue', 'red', 'green', 'black', 'white']
vehicle1 = Sedan('Fedos', 'Toyota Mark II', 'blue', 500)

# Initial properties
vehicle1.print_info()

# Changing properties (including calling methods)
vehicle1.set_color('Pink')
vehicle1.set_color('BLACK')
vehicle1.owner = 'Vasyok'

# Let's check what has changed
vehicle1.print_info()
