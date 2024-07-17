def is_prime(func):
    def wrapper(*args, **kwargs):
        # If given number is greater than 1
        res = func(*args, **kwargs)
        if res > 1:
            # Iterate from 2 to n // 2
            for i in range(2, (res // 2) + 1):
                # If num is divisible by any number between
                # 2 and n / 2, it is not prime
                if (res % i) == 0:
                    print("is not a prime number")
                    break
            else:
                print("is a prime number")
        else:
            print("is not a prime number")
        return res

    return wrapper


@is_prime
def sum_three(x, y, z):
    return x + y + z


# test
result = sum_three(2, 3, 6)
print(result)
