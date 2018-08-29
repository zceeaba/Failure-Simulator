from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.Node import Node
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.key import key
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.Ring import Ring


import numpy as np
import random
import networkx as nx
from matplotlib import pyplot as plt
import string
import random
random.seed(3)


##https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf


class ChordFailures(FailureMode):

    def id_generator(self,size=6, chars=string.ascii_uppercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def ip_generator(self,start_ip,end_ip):
        start = list(map(int, start_ip.split(".")))
        end = list(map(int, end_ip.split(".")))
        temp = start
        listofips = []

        listofips.append(start_ip)
        while temp != end:
            start[3] += 1
            for i in (3, 2, 1):
                if temp[i] == 256:
                    temp[i] = 0
                    temp[i - 1] += 1
            listofips.append(".".join(map(str, temp)))

        return listofips

    def draw_topology(self,topology):
        pos = nx.spring_layout(topology)
        nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
        plt.show()

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))

        new_topology = topology.copy()
        to_be_deleted = []

        keys=[self.id_generator() for i in range(0,30)]
        nodes=self.ip_generator("192.168.1.0", "192.171.3.25")

        ring=Ring()

        for node in nodes:
            newNode=Node(node)
            ring.nodeslist.append(newNode)

        print(ring.nodeslist)






