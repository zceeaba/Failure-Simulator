from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import random


class NatFailure(FailureMode):

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))

        num_nodes = round(0.73*len(topology.nodes))

        new_topology = topology.copy()
        to_be_deleted = []
        for i in range(0, int(num_nodes)):
            tnk=list(topology.nodes.keys())
            delete = random.choice(list(topology.nodes.keys()))
            print(delete)
            while delete in to_be_deleted:
                delete = random.choice(list(topology.nodes.keys()))
            to_be_deleted.append(delete)

        for n in to_be_deleted:
            new_topology.remove_node(n)
        return new_topology