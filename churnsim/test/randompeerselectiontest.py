from nxsim import NetworkSimulation
from churnsim.uk.ac.bristol.rechurn.modes.p2p.bittorrent.randompeerselection import randompeerfailure
from networkx import nx
import string
import random

numberofnodes=3000
G = nx.complete_graph(numberofnodes)

nodes=[dict() for x in range(numberofnodes)]

keys=range(numberofnodes)

for i in keys:
    nodes[i]["pieces"]=[]
    nodes[i]["id"]=0
    nodes[i]["peerid"]=i
    nodes[i]["downloadlist"]=[]
    nodes[i]["uploadlist"]=[]


seednode=random.randint(0,numberofnodes)

hashdata=string.ascii_letters

for i in range(10):
    piece={"pieceid":random.choice(hashdata),"piecesize":0.1}
    nodes[seednode]["pieces"].append(piece)

nodes[seednode]["id"]=1


sim=NetworkSimulation(topology=G,agent_type=randompeerfailure,states=nodes,
                     num_trials=3,max_time=10,logging_interval=1.0)


sim.run_simulation()
