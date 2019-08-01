from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import numpy as np
import random
import networkx as nx
from matplotlib import pyplot as plt

#https://www.inf.ed.ac.uk/teaching/courses/es/PDFs/lecture_9.pdf
#https://www.ntt-review.jp/archive/ntttechnical.php?contents=ntr201209ra1.html

class weibullfailures(FailureMode):
    def __init__(self,mttfalgorithm,time):
        self.survived=False
        self.mttfalgorithm=mttfalgorithm
        self.time=time

    def core_survived(self,percent):
        survived = False
        rand = (random.uniform(0,1) * 100)
        if ((rand < percent) or (rand == percent)):
            survived = True

        return survived

    def get_failure_probability(self,wearout,t):
        newpercent = 0
        if wearout == False:
            percent = (np.exp(-(0.0003 * t)))
            newpercent = percent * 100.0
        else:
            newLambda = (t * (0.0003 * 0.0003))
            percent = (np.exp(-(newLambda * t)))
            newpercent = percent * 100.0

        return newpercent


    def mttf(self,length):
        trial_results = {}
        x = 0
        survived = False

        while (x < length):
            t = 0
            wearout=False
            while (t < 100):
                prob = self.get_failure_probability(wearout,t)
                survived = self.core_survived(prob)
                if t==99:
                    trial_results[x]=t
                    x = x + 1
                    break
                elif (survived == True):
                    t=t+1
                else:
                    trial_results[x] = t
                    x = x + 1
                    wearout=True
                    break

        return trial_results

    def draw_topology(self,pos,topology):
        nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
        plt.show()

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))
        pos = nx.spring_layout(topology)
        new_topology = topology.copy()
        to_be_deleted = []

        failuretimes=self.mttf(len(topology.nodes))
        deletelength=0

        if self.mttfalgorithm==True:
            t=0
            nodeslist=list(new_topology.nodes)
            while(t<self.time):
                count=0
                for i in failuretimes:
                    if failuretimes[i]==t:
                        new_topology.remove_node(nodeslist[count])
                        deletelength+=1
                    count+=1
                self.draw_topology(pos,new_topology)
                t=t+1

        else:
            num_nodes = (np.random.randint(0, len(topology.nodes)))

            if num_nodes < 10:
                num_nodes = 10

            num_nodes = num_nodes * 0.1  # max 10% churn

            for i in range(0, int(num_nodes)):
                tnk=list(topology.nodes.keys())
                delete = np.random.weibull(list(topology.nodes.keys()),len(topology.nodes))
                while delete in to_be_deleted:
                    delete = np.random.weibull(list(topology.nodes.keys()),len(topology.nodes))
                to_be_deleted.append(delete)

            for n in to_be_deleted:
                new_topology.remove_node(n)

        return deletelength
