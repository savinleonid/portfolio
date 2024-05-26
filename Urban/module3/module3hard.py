# test data
data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]


def calculate_structure_sum(*structure):
    """
    Takes structured data and calculates sum of all integers and cumulative length of strings in it recursively
    :param structure:
    :return: int
    """
    sum_ = 0  # initialize sum
    for arg in structure:  # iterate over all sub structures
        # We will operate summation recursively.
        # First, find final int or str values and operate relatively
        if isinstance(arg, dict):  # in dict case we need to access to values too
            for i in arg.values():
                # separate 'str' and 'int' cases
                if isinstance(i, int):
                    sum_ += i
                elif isinstance(i, str):
                    sum_ += len(i)
        if isinstance(arg, int):
            sum_ += arg
        elif isinstance(arg, str):
            sum_ += len(arg)
        else:
            # Recursive entry.
            sum_ += calculate_structure_sum(*arg)  # get partial sum of sub structure
    return sum_  # return final sum


# test
result = calculate_structure_sum(data_structure)
print(result)
