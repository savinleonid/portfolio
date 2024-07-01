def add_everything_up(a, b):
    """
    Returns either sum of given numbers or concatenated string of given parameters if they are not summable
    :param a: Any,
    :param b: Any,
    :return: a + b or str['ab']
    """

    #  catch exception if it's not summable
    try:
        return a + b
    except TypeError:
        return str(a) + str(b)  # reverse all parameters to string and concatenate them


#  test
print(add_everything_up(123.456, 'string'))
print(add_everything_up('apple', 4215))
print(add_everything_up(123.456, 7))
