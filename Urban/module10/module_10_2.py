from threading import Thread
from time import sleep


class Knight(Thread):  # inherited class from Thread
    def __init__(self, name, power):
        super().__init__()  # Thread class initialisation
        self.name: str = name
        self.power: int = power
        self.enemy = 100
        self.days = 0

    def run(self):  # overriding run method in inherited class Thread
        print(f"{self.name}, we've been attacked!")
        while self.enemy > 0:
            self.enemy -= self.power
            sleep(1)  # one second - one day
            self.days += 1
            print(f"{self.name} has been fighting for {self.days} days, {self.enemy} enemy left.")
        print(f"{self.name} was victorious after {self.days} days!")


# test
first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

# start
first_knight.start()
second_knight.start()

# wait until all done
first_knight.join()
second_knight.join()

print("All fights ended!")
