def decipher(num: int):
    """
    Decipher.
    Finds corresponding password solution for final additional homework module 2.
    Takes integer from 3 to 20 and returns concatenated password string of unique pairs that sum of each
    is equal to subdivides of given number.

    :param num: int
    :return str:
    """
    if 3 <= num < 20 and isinstance(num, int):
        # start operations
        password = []  # unique pairs will store here before concatenation
        for i in range(1, num):  # first literal of pair. We don't want it to start with '0' so start from 1
            for j in range(i, num):  # second literal of pair. Start iterating from first literal to get uniqueness
                if num % (i + j) == 0 and (i != j):  # check for subdivision condition
                    password.append(str(i) + str(j))  # store concatenated pair in list

        return str.join("", password)  # convert list values to string
    else:
        # if number is invalid
        print("Invalid number. Must be an integer between 3 - 19(inclusive)")  # can go to log or raise error
        return None


# test
for n in range(2, 20):
    psw = decipher(n)
    print(f"{n}-", psw)
