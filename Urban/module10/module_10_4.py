import time
from queue import Queue
from threading import Thread


class Table:
    available = {}

    def __init__(self, number):
        self.number: int = number
        self.is_busy: bool = False  # initially not busy
        # init all tables as available
        for i in range(number):
            Table.available[i + 1] = True


class Cafe:
    def __init__(self, tables):
        self.queue = Queue()
        self.tables = tables

    def dequeue(self):
        """To finish serving all last customers"""
        while not self.queue.empty():
            while not any(Table.available.values()):  # wait until at least one table available
                time.sleep(0.1)  # little threshold for not to overclock cpu
            self.serve_customer(None)  # handle single customer in queue if there is

    def customer_arrival(self):
        for i in range(20):  # limiting customers to 20
            customer = Customer(i + 1, None)  # first we need create customer without table
            print(f"Customer number {customer.number} has arrived.")
            self.serve_customer(customer)  # will serve this customer if there is no one in queue
            # put in queue if no tables available and if customer not served
            if not any(Table.available.values()) and not customer.is_served:
                self.queue.put(customer)  # put in queue
                print(f"Customer number {customer.number} is waiting for empty table.")
            time.sleep(1)  # customers will arrive every second
        self.dequeue()  # finish last customers in queue

    def serve_customer(self, customer):
        for table in self.tables:  # loop through all tables to check availability
            if not table.is_busy:
                table.is_busy = True
                table.available[table.number] = False
                # serve customer from queue if there is, else continue with default
                if not self.queue.empty():
                    customer = self.queue.get()
                customer.table = table  # pass table info to customer class to handle availability in each customer
                customer.start()  # start serving with thread
                break  # breaks for loop when finds empty table


class Customer(Thread):
    def __init__(self, number, table):
        super().__init__()
        self.number = number
        self.table = table
        self.is_served = False  # extra flag for handling 'getting in queue' information. Initially false

    def run(self):
        self.is_served = True
        print(f"Customer number {self.number} sat down at table number {self.table.number}.")
        time.sleep(5)  # serving for 5 seconds
        print(f"Customer number {self.number} ate and left.")
        self.table.is_busy = False
        self.table.available[self.table.number] = True


# test
# creating 3 table
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# cafe initialisation
cafe = Cafe(tables)

# start thread for customer arrival
customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# wait for completion of arrival customers
customer_arrival_thread.join()
