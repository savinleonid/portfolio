def custom_write(file_name, strings):
    line = 1
    strings_positions = {}
    with open(file_name, "w", encoding="utf-8") as file:
        for string in strings:
            strings_positions[(line, file.tell())] = string
            file.write(string + '\n')
            line += 1
    return strings_positions


# test
info = [
    'Text for tell.',
    'Используйте кодировку utf-8.',
    'Because there are 2 languages!',
    'Спасибо!'
]

result = custom_write('test.txt', info)
for elem in result.items():
    print(elem)
