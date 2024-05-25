def test_function():
    def inner_function():
        print("Я в области видимости функции test_function")
    inner_function()


# test
test_function()

inner_function()  # :Unresolved reference 'inner_function' - cant access because of different namespaces
