"""Using the map and filter functions to leave odd square numbers in the final list"""
list_ = [1, 2, 5, 7, 12, 11, 35, 4, 89, 10]

list_ = list(map(lambda x: x**2, filter(lambda x: x % 2, list_)))
print(list_)
