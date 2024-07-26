from multiprocessing import Process, Queue


class WarehouseManager:
    def __init__(self):
        super().__init__()
        self.data = {}
        self.queue = Queue()  # for subprocess communication

    def process_request(self, request: tuple, data):
        """Processing single change request of warehouse inventory data"""
        product, method, amount = request
        self.data = data
        if method == "receipt":  # in case of adding
            if product in self.data.keys():  # check if there is already same product, add if not
                self.data[product] += amount
            else:
                self.data[product] = amount
        elif method == "shipment":  # in case of removing
            if product in self.data.keys() and self.data[product] > 0:  # check if product exists and bigger than 0
                self.data[product] -= amount
        # only two method allowed, otherwise raise exception
        else:
            raise Exception("Bad request")
        self.queue.put(self.data)  # communication between processes

    def run(self, requests):
        """Starts individual subprocess for each request"""
        procs = []
        for request in requests:
            # we need to pass 'self.data' to each process!!!
            proc = Process(target=self.process_request, args=(request, self.data,))
            proc.start()
            procs.append(proc)
            self.data = self.queue.get()  # communication between processes
        # not really necessary, but still...
        for proc in procs:
            proc.join()


if __name__ == "__main__":
    # initialising manager
    manager = WarehouseManager()

    # multiple requests
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # start processing requests
    manager.run(requests)

    # displaying updated data on warehouse stocks
    print(manager.data)
