from threading import Thread, Lock

# thread locks to prevent race conditions
deposit_lock = Lock()
withdraw_lock = Lock()


class BankAccount(Thread):
    def __init__(self):
        super().__init__()
        self.balance = 1000  # initial balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}, new balance is {self.balance}")

    def withdraw(self, amount):
        self.balance -= amount
        print(f"Withdrew {amount}, new balance is {self.balance}")


def deposit_task(acc, amount):
    for _ in range(5):
        with deposit_lock:  # using lock w/ context manager 'with'
            acc.deposit(amount)


def withdraw_task(acc, amount):
    for _ in range(5):
        with withdraw_lock:  # using lock w/ context manager 'with'
            acc.withdraw(amount)


# test
account = BankAccount()

deposit_thread = Thread(target=deposit_task, args=(account, 100))
withdraw_thread = Thread(target=withdraw_task, args=(account, 150))

deposit_thread.start()
withdraw_thread.start()

deposit_thread.join()
withdraw_thread.join()
