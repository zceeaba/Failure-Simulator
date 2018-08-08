from nxsim import NetworkSimulation
#from churnsim.uk.ac.bristol.rechurn.modes.p2p.biasedpeerselection import biasedpeerfailure
from networkx import nx
import random

numberofnodes=10
G = nx.complete_graph(numberofnodes)

failurestates={}
keys=range(numberofnodes)

for i in keys:
    failurestates[i]=0

failurenode=random.randint(0,numberofnodes)

failurestates[failurenode]=1

sim=NetworkSimulation(topology=G,agent_type=randompeerselection,states=,environment_agent=,dir_path=,
                      num_trials=,max_time=,logging_interval=)