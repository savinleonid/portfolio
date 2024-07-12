class StepValueError(ValueError):  # custom value error exception class
    pass


class Iterator:
    def __init__(self, start, stop, step=1):
        self.start = start  # inclusive
        self.stop = stop  # inclusive
        self.step = step
        self.pointer = start  # initially at start

        if step == 0:
            raise StepValueError('Step can not be equal to zero')

    def __iter__(self):
        self.pointer = self.start - self.step  # initialize pointer to start and shift 1 step to include first value
        return self  # return iterator itself

    def __next__(self):  # magic class to get next value in iterator
        # since we cant increase pointer by one step after return statement, we need to shift it back at first use to
        # include first value. we made it in __iter__ method.
        self.pointer += self.step

        # stop cases are different for 'stop' argument's sign, so we need to separate them
        if self.step > 0:
            if self.pointer > self.stop:
                raise StopIteration
        elif self.step < 0:
            if self.pointer < self.stop:
                raise StopIteration
        return self.pointer  # eventually we return current value


# test
try:
    iter1 = Iterator(100, 200, 0)  # wrong step
    for i in iter1:
        print(i, end=' ')
except StepValueError:
    print('Step is wrong')

iter2 = Iterator(-5, 1)
iter3 = Iterator(6, 15, 2)
iter4 = Iterator(5, 1, -1)
iter5 = Iterator(10, 1)


for i in iter2:
    print(i, end=' ')
print()
for i in iter3:
    print(i, end=' ')
print()
for i in iter4:
    print(i, end=' ')
print()
for i in iter5:
    print(i, end=' ')
print()
