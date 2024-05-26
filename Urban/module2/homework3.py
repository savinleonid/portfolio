def print_params(*args, **kwargs):  # function prints out parameters 2 times
    print(*args, **kwargs)
    print(*args, **kwargs)


telephony = {"Leonid": "950000111222"}  # test dict

# outputs
print_params("My name is Leo")
print_params(123)
print_params("Is True?: ", True)
print_params(*telephony, telephony)
print_params(*telephony.values())
