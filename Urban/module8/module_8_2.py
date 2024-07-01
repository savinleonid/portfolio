def personal_sum(numbers):
    """
    Returns sum of valid number collection and number of incorrect type for sum operation.
    :param numbers: iterable data collection
    :return: (result, incorrect_data)
    """
    result = 0
    incorrect_data = 0
    for num in numbers:
        try:
            result += num
        except TypeError:
            print("Incorrect type for sum operation -", num)
            incorrect_data += 1
    return result, incorrect_data


def calculate_average(numbers):
    """
    Calculates mean of valid numbers w/ personal_sum() function. Returns 'None' if given type is not collection.
    :param numbers: iterable data collection
    :return: mean of valid numbers
    """
    try:
        res, incorrect_data = personal_sum(numbers)
        return res / (len(numbers) - incorrect_data)
    except ZeroDivisionError:
        return 0
    except TypeError as exc:
        print("There is incorrect type in numbers")


# test
print(f'Result 1: {calculate_average("1, 2, 3")}')  # String iterating, but each symbol is string
print(f'Result 2: {calculate_average([1, "String", 3, "One more string"])}')  # 1 и 3 only
print(f'Result 3: {calculate_average(567)}')  # wrong type
print(f'Result 4: {calculate_average([42, 15, 36, 13])}')  # Works fine
