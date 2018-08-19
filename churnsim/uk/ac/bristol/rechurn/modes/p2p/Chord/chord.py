from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import numpy as np
import random
import networkx as nx
from matplotlib import pyplot as plt
import hashlib

#https://www.inf.ed.ac.uk/teaching/courses/es/PDFs/lecture_9.pdf
#https://www.ntt-review.jp/archive/ntttechnical.php?contents=ntr201209ra1.html

class ChordFailures(FailureMode):

    def draw_topology(self,topology):
        pos = nx.spring_layout(topology)
        nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
        plt.show()

    def chord_hash(self,keystring):
        hashedobj=hashlib.sha1(keystring)
        return hashedobj.hexdigest()

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))

        new_topology = topology.copy()
        to_be_deleted = []


