immutable_var = (0.0, 1, [2, 3], (4, 5,), "string", True)  # init tuple w/ different types
print("Tuple:", immutable_var)  # print tuple
print("Inside Tuple:",
      immutable_var[0],
      immutable_var[1],
      immutable_var[2],
      immutable_var[3],
      immutable_var[4],
      immutable_var[5],
      )  # Tuples accessible

try:
    immutable_var[0] = 2.0  # Tuples doesn't support item assignment!!! Will raise TypeError.
except TypeError as e:
    print(e)

mutable_list = [0.0, 1, [2, 3], (4, 5,), "string", True]  # # init list w/ different types
print("List", mutable_list)  # print list

mutable_list.append(False),  # append list item to end of list
print(mutable_list)
mutable_list.remove(1),  # remove exact item
print(mutable_list)
mutable_list.extend(["extend", "list"])  # extends list by list
print(mutable_list)
# List's accessible and changeable
