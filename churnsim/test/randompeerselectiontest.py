from nxsim import NetworkSimulation
from churnsim.uk.ac.bristol.rechurn.modes.p2p.randompeerselection import randompeerfailure
from networkx import nx
import random
from collections import defaultdict

numberofnodes=10
G = nx.complete_graph(numberofnodes)

failurestates=[dict() for x in range(numberofnodes)]

keys=range(numberofnodes)

for i in keys:
    failurestates[i]["piecesize"]=0
    failurestates[i]["id"]=0

failurenode=random.randint(0,numberofnodes)

failurestates[failurenode]["piecesize"]=1
failurestates[failurenode]["id"]=1

print(failurestates)



sim=NetworkSimulation(topology=G,agent_type=randompeerfailure,states=failurestates,
                     num_trials=30,max_time=30,logging_interval=1.0)

sim.run_simulation()
