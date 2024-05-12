from operator import truediv

# initialization
grades = [[5, 3, 3, 5, 4], [2, 2, 2, 3], [4, 5, 5, 2], [4, 4, 3], [5, 5, 5, 4, 5]]
students = {'Johnny', 'Bilbo', 'Steve', 'Khendrik', 'Aaron'}

students = list(students)  # revert to list for accessibility
students.sort()  # sort alphabetically
grades = map(truediv, list(map(sum, grades)), list(map(len, grades)))  # find mean of sublists and reassign to grades
dict_grades = dict(zip(students, grades))  # zip list and map dict

print(dict_grades)
