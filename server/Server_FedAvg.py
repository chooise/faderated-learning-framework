import time

import numpy as np

from server.Server import *


class Server_FedAvg(Server):
    def __init__(self, args, dataset_test, net_glob):
        super().__init__(args, dataset_test, net_glob)
        self.m = int(self.args.client_nums * self.args.frac)
        self.cache = [None for _ in range(self.m)]

    def main(self):
        start_time = time.time()

        while time.time() - start_time < self.args.limit_time:
            sample_clients = np.random.choice(self.idle_client, self.m, replace=False)

            for client in sample_clients:
                self.dispatch(client)

            num_of_received_model = 0
            while num_of_received_model < self.m:
                model, client_idx = self.receiveUpdate()
                num_of_received_model += 1

            self.aggregation(self.cache, [])

            self.test()