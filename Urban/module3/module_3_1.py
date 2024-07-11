calls = 0  # global variable for function call record


def count_calls():
    """Counter for function call using global variable 'calls'."""
    global calls
    calls += 1


def string_info(string: str):
    """
    Returns string info.
    :param string:
    :return: tuple[length of string, upper string, lower string]
    """
    count_calls()  # recording call number
    return len(string), string.upper(), string.lower()


def is_contains(string: str, list_to_search: list):
    """
    Checks if string contains in given list.
    :param string:
    :param list_to_search:
    :return: True if string exist, False if not
    """
    count_calls()  # recording call number
    return True if string.lower() in str(list_to_search).lower() else False


# test
print(string_info('Capybara'))
print(string_info('Armageddon'))
print(is_contains('Urban', ['ban', 'BaNaN', 'urBAN']))  # Urban ~ urBAN
print(is_contains('cycle', ['recycling', 'cyclic']))  # No matches
print(calls)
