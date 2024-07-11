from random import choice

# ---lambda function---
first = 'Мама мыла раму'
second = 'Рамена мало было'

# test
print(list(map(lambda x, y: x == y, first, second)))


# ---closure---
def get_advanced_writer(file_name):
    def write_everything(*data_set):
        with open(file_name, "a", encoding="utf8") as f:
            for data in data_set:
                f.write(str(data) + '\n')

    return write_everything


# test
write = get_advanced_writer('example.txt')
write('Это строчка', ['А', 'это', 'уже', 'число', 5, 'в', 'списке'])


# --- __call__ method ---
class MysticBall:
    def __init__(self, *words):
        self.words = words

    def __call__(self):
        return choice(self.words)


# test
first_ball = MysticBall('Да', 'Нет', 'Наверное')
print(first_ball())
print(first_ball())
print(first_ball())
