from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import numpy as np
from scipy.stats import expon
import networkx as nx
import matplotlib.pyplot as plt

#FailureSim: A System for Predicting Hardware Failures in Cloud Data Centers Using Neural Networks
#http://fta.scem.uws.edu.au/pub/fta_ccgrid10_pres.pdf
#http://www.cs.cmu.edu/~bianca/fast07.pdf
#Refer to http://www.netlib.org/utk/people/JackDongarra/PAPERS/Cloud-Shaun-Jack.pdf
#https://github.com/Cloudslab/iFogSim
#https://www.microsoft.com/en-us/research/wp-content/uploads/2010/06/socc088-vishwanath.pdf
#http://opac.vimaru.edu.vn/edata/EBook/TAILIEUSO/ACM/ACM%20Transactions%20on%20Storage/a6-sankar.pdf

class hardwarefailure(FailureMode):

    def calculateweibull(self,reliability,length):
        return np.random.weibull(reliability,length)

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))
        num_nodes=len(topology.nodes)

        pos = nx.spring_layout(topology)
        nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
        plt.show()

        """
        workload={}
        nodereliability={}

        deletenodes=[]
        for x in topology:
            if topology.node[x]["type"]=="FOG_DEVICE":
                edges=list(nx.neighbors(topology,x))
                latencysum=0
                reliabilitysum=0
                for j in edges:
                    memory=topology.node[x]["ram"]
                    mips = topology.node[x]["mips"]
                    bandwidth = topology.node[x]["downBW"]
                    ts=workload[j]/mips
                    tc=memory/bandwidth
                    latency = topology[x][j]["latency"]
                    latencysum+=latency
                    reliabilitysum+=(ts+tc)
                if reliabilitysum<latencysum:
                    deletenodes.append(x)
                nodereliability[x]=reliabilitysum

        deleteweibull=self.calculateweibull()
        """

        return topology

