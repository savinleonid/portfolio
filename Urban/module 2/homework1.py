x = 38

print("Hi!")
if x < 0:
    print("Less then 0")
print("Bye!")

######################

# examples
a, b = 10, 5

if a > b:
    print("a > b")

if a > b and a > 0:
    print("success")

if (a > b) and (a > 0 or b < 1000):
    print("success")

if 5 < b and b < 10:
    print("success")

######################

# comparable - numbers, strings, lists
if "34" > "123":
    print("success")

if "123" > "12":
    print("success")

if [1, 2] > [1, 1]:
    print("success")

######################

# not comparable - different types
if "6" > 5:
    print("success")

if [5, 6] > 5:
    print("success")

if "6" != 5:
    print("success")
