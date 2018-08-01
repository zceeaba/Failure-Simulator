from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import numpy as np
from scipy.stats import expon

class temperaturefailures(FailureMode):
    def get_new_topology(self,topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))

        Ro=10^(-6)
        num_nodes = (Ro*np.random.exponential(len(topology.nodes)))
        if num_nodes < 10:
            num_nodes = 10

        num_nodes = num_nodes * 0.1 # max 10% churn
        new_topology = topology.copy()
        to_be_deleted = []
        for i in range(0, int(num_nodes)):
            delete = np.random.choice(topology.nodes.keys())
            while delete in to_be_deleted:
                delete = np.random.choice(topology.nodes.keys())
            to_be_deleted.append(delete)
        for n in to_be_deleted:
            new_topology.remove_node(n)
        return new_topology