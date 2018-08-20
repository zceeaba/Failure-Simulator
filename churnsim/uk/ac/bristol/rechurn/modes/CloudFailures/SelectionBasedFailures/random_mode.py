from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import random
import networkx as nx
import matplotlib.pyplot as plt
import re


class RandomFailures(FailureMode):

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))
        count=0
        pos = nx.spring_layout(topology)
        nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
        plt.show()

        while count<10:
            num_nodes = (random.randint(0, len(topology.nodes)))
            if num_nodes < 10:
                num_nodes = 10

            num_nodes = num_nodes * 0.1 # max 10% churn
            new_topology = topology.copy()

            nodes=topology.nodes

            """
            pos = nx.spring_layout(topology)
            nx.draw(topology, pos, with_labels=True, arrows=False, node_size=1000)  # generic graph layout
            nodelist = [x for x in nodes if re.search('pe[0-9]', x)]  # create a list containing PE nodes only
            nx.draw_networkx_nodes(topology, pos, nodelist=nodelist, node_color='b',
                                   node_size=1000)  # change PE node colour to blue
            nx.draw_networkx_edge_labels(topology, pos)  # draw edge labels
            plt.savefig('topology_result.png')
            """

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

            pos = nx.spring_layout(topology)
            nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
            plt.show()

            topology=new_topology
            count+=1

        return new_topology