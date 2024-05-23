# init dict
my_dict = {
    "name": "Leonid",
    "surname": "Savin"
}

print("Dict:", my_dict)  # prints whole structure
print("Existing value:", my_dict["name"])  # access value by call
print("Not existing value:", my_dict.get("year"))  # return None if not exist

# add two more keywords
my_dict.update({
    "birth_date": 1994,
    "age": 29
})

print("Deleted value:", my_dict.pop("surname"))  # delete and print it's value

# print dict again
print("Modified dictionary:", my_dict)


# init set
my_set = {
    "string",
    "string",
    1,
    1,
    2.5,
    2.5,
    True,
    True
}

print("Set:", my_set)  # # prints whole structure

# add two more unique values
my_set.update({
    False,
    "Leonid"
})

my_set.remove(True)  # remove value of set
print("Modified set:", my_set)  # print updated set
