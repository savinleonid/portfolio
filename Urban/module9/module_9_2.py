# fabric function for base operations
def create_operation(operation):
    if operation == "add":
        def add(x, y):
            return x + y

        return add  # return function, not object!! no parenthesis needed
    elif operation == "subtract":
        def subtract(x, y):
            return x - y

        return subtract
    elif operation == "divide":
        def divide(x, y):
            try:
                return x / y
            except ZeroDivisionError:
                print("ERROR: Division by zero")

        return divide
    elif operation == "multiply":
        def multiply(x, y):
            return x * y

        return multiply


my_func_add = create_operation("add")  # get 'add' function
print("Fabric function:", my_func_add(1, 2))  # call 'add' function and get 3

# example of a lambda function with an analogue via def
sqr = lambda x: x ** 2  # square the number via lambda
print("Lambda function:", sqr(3))  # gets 9


def sqr_def(x):
    return x ** 2


print("Analogue def function:", sqr_def(3))  # gets 9


# the Rect class with attributes a, b, which are set in __init__, and a __call__ method, which returns the area of the
# rectangle, that is, a*b.
class Rect:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        return self.a * self.b  # return area when called


rect = Rect(2, 4)
print("'__call__' method:", rect())  # gets 8
