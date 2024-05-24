def test(*args):
    """Prints each argument"""
    for arg in args:
        print(arg)


test(1, "Hi", True)


def factorial(n: int):
    """
    Multiplies a number by every number below it till 1
    :param n: Positive integer
    :return: int: n >= 0, None: n < 0
    """
    if n == 1:
        return 1
    elif n == 0:
        return 0
    elif n < 0:
        print("Function needs positive integer input")
        return None
    else:
        return n * factorial(n - 1)


print("Positive:", factorial(5))  # positive test
print("Zero:", factorial(0))  # zero test
print("Negative:", factorial(-1))  # negative test
