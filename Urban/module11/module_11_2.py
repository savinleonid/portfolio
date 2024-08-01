import inspect


def introspection_info(obj):
    info = {}
    methods = []
    magic_methods = []
    attr = []
    magic_attr = []
    for member in inspect.getmembers(obj):
        if member[0].startswith('__') and member[0].endswith('__'):  # magic members
            if inspect.ismethod(member[1]):
                magic_methods.append(member[0])
            else:
                magic_attr.append(member[0])
        else:
            if inspect.ismethod(member[1]):
                methods.append(member[0])
            else:
                attr.append(member[0])
    info["type"] = type(obj)
    info["methods"] = methods
    info["attributes"] = attr
    info["magic methods"] = magic_methods
    info["magic attributes"] = magic_attr
    info["module"] = inspect.getmodule(obj)
    return info


class NewClass(object):
    def __init__(self, number):
        self.multi = int(number) * 2
        self.str = str(number)
        self.__test = 1

    def func_1(self):
        pass


# test
x = NewClass(5)
number_info = introspection_info(x)
print(number_info)
