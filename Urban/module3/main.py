"""
namespace testing
"""
# GLOBAL VARIABLES
a = 5
b = 10
c = 15


def test():
    # LOCAL VARIABLES
    a = 1  # Shadows name 'a' and 'b' from outer scope because they same in local and global.
    b = 2  # Better to rename them, but not critical
    print(a, b)


def test2(x, y, z):
    print(x, y, z)


# prints locals
test()

# prints global
test2(a, b, c)  # although 'a' and 'b' declared in function, results was global.
# because we cant access local variables outside function they created
