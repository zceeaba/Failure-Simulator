from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import numpy as np
from scipy.stats import expon
import networkx as nx

#Refer to http://www.netlib.org/utk/people/JackDongarra/PAPERS/Cloud-Shaun-Jack.pdf
#https://www.ntt-review.jp/archive/ntttechnical.php?contents=ntr201209ra1.html
#https://github.com/Cloudslab/iFogSim

class hardwarefailure(FailureMode):

    def calculateweibull(self,reliability,length):
        return np.random.weibull(reliability,length)

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))
        num_nodes=len(topology.nodes)

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

        return topology

