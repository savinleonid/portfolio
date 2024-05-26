def print_params(a=1, b='string', c=True):
    print(f"First param: {a},\n"
          f"Second param: {b},\n"
          f"Third param: {c}\n")


# default param test --------------------------------
print_params()

# different types with initial and last default value test
print_params("test", 5)  # will give warning because of different types with initial typing, not critical

# unpacking test
print_params(1,*["test", False])

# other tests
print_params(b=25)  # will give warning because of different types with initial typing, not critical
print_params(c = [1,2,3])  # changes only last parameter

# unpacking ---------------------------------------

values_list = [True, "string", 10]  # 3 different type values list
# dict associated w/ function 'print_params' but with different value types
values_dict = {
    "a": False,
    "b": 2,
    "c": "test"
}

# unpacking test
print_params(*values_list)
print_params(**values_dict)
# although different types with initial typing, no warning was given

# other tests
values_list_2 = [True, 2.0]
print_params(*values_list_2, 42)  # working as expected
