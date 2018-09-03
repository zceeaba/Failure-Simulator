#http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=F5A14DDDCF298111712CAA63BF5B762B?doi=10.1.1.685.1060&rep=rep1&type=pdf
#https://users.ece.cmu.edu/~koopman/des_s99/sw_reliability/
#https://www.slideshare.net/AnandKumar87/software-reliability-11841804
#https://ieeexplore.ieee.org/document/8004398/
#https://pdfs.semanticscholar.org/presentation/be40/f5b035534ccc756a821eb2fd6108e09bbf65.pdf

from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import random
import networkx as nx
from matplotlib import pyplot as plt
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.SoftwareFailures.Gossip import GossipNode
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.SoftwareFailures.Task import Task
from scipy import optimize



class SoftwareFailures(FailureMode):

    def __init__(self,time,capacities=None):
        self.capacities=capacities
        self.time=time

    def draw_topology(self,topology):
        pos = nx.spring_layout(topology)
        nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
        plt.show()

    def generateworkloadsizes(self,size):
        ws = [Task(i, random.randint(2000, 2500)) for i in range(0, size)]
        return ws


    def get_new_topology(self, topology):
        """
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))
        """
        deletecountlist=[]
        capastarts=[i for i in range(100,500,100)]




        for i in capastarts:
            capacities = [random.randint(i, i+10) for j in range(0, len(topology.nodes))]
            new_topology = topology.copy()
            to_be_deleted = []
            GossipNodelist=list(new_topology.nodes)
            graphtogossip={}

            count=0
            for x in GossipNodelist:
                graphtogossip[x]=GossipNode(x,capacities[count])
                count+=1

            workload = self.generateworkloadsizes(self.time)

            deletecount=0
            #start monte carlo loop
            t=0

            while t<self.time:
                chosenindex=random.randint(0,(len(new_topology.nodes)-1))
                chosennode=GossipNodelist[chosenindex]
                gpobject=graphtogossip[chosennode]
                currentworkload=workload[t]
                gpobject.assigntask(currentworkload,t)
                if gpobject.failure==1:
                    new_topology.remove_node(chosennode)
                    GossipNodelist = list(new_topology.nodes)
                    deletecount+=1

                #self.draw_topology(new_topology)
                t=t+1

            print(deletecount)
            deletecountlist.append(deletecount)

            return deletecount














