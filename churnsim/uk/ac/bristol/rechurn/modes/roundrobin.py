from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import random


class RandomFailures(FailureMode):

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))

        num_nodes = (len(topology.nodes))
        if num_nodes < 10:
            num_nodes = 10

        num_nodes = num_nodes * 0.1 # max 10% churn
        new_topology = topology.copy()
        to_be_deleted = []
        j=0
        for i in range(0, int(num_nodes)):
            delete=topology.nodes[j%num_nodes]
            j+=1
            to_be_deleted.append(delete)

        for n in to_be_deleted:
            new_topology.remove_node(n)
        return new_topology