my_list = ["banana", "apple", "kiwi", "orange", "lemon", "strawberry"]  # init list
print("My List:", my_list)  # print list
print("First Element:", my_list[0])  # first element
print("Last Element:", my_list[-1])  # last element
print("Sublist:", my_list[2:4])  # sublist from 3 to 5(not inclusive)
my_list[2] = "CHANGED"  # change 3. element of list
print("Changed List:", my_list)  # updated list

my_dict = {'go': 'идти', 'run': 'бежать', 'first': 'первый'}  # init dict
print("My Dict:", my_dict)  # print dict
print("Run>>", my_dict.get('run'))  # print value, 'get()' returns value
my_dict['go'] = 'идти CHANGED'  # assignment
print("Sleep>>", my_dict.setdefault('sleep', 'спать'))  # # print value, 'setdefault()' returns value
print("Changed dict:", my_dict)
