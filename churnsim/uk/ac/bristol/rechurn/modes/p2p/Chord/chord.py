from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.Node import Node
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.key import key
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.ring import ring


import numpy as np
import random
import networkx as nx
from matplotlib import pyplot as plt

##https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf


class ChordFailures(FailureMode):

    def draw_topology(self,topology):
        pos = nx.spring_layout(topology)
        nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
        plt.show()

    def assignkeytonode(self,key,Node):


    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))

        new_topology = topology.copy()
        to_be_deleted = []




