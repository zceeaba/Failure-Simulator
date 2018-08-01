from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import numpy as np

class weibullfailures(FailureMode):
    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))

        num_nodes = (np.random.randint(0, len(topology.nodes)))
        if num_nodes < 10:
            num_nodes = 10

        num_nodes = num_nodes * 0.1 # max 10% churn
        new_topology = topology.copy()
        to_be_deleted = []
        for i in range(0, int(num_nodes)):
            tnk=list(topology.nodes.keys())
            delete = np.random.weibull(list(topology.nodes.keys()),len(topology.nodes))
            print(delete)
            print(to_be_deleted)
            while delete in to_be_deleted:
                delete = np.random.weibull(list(topology.nodes.keys()),len(topology.nodes))
            to_be_deleted.append(delete)

        for n in to_be_deleted:
            new_topology.remove_node(n)

        return new_topology
