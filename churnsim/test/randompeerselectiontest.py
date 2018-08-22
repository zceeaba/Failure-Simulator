from nxsim import NetworkSimulation
from churnsim.uk.ac.bristol.rechurn.modes.p2p.bittorrent.randompeerselection import randompeerfailure,faileddict
from networkx import nx
import string
import random
from matplotlib import pyplot as plt

numberofnodes=100
G = nx.complete_graph(numberofnodes)

nodes=[dict() for x in range(numberofnodes)]

keys=range(numberofnodes)

for i in keys:
    nodes[i]["pieces"]=[]
    nodes[i]["id"]=0
    nodes[i]["peerid"]=i
    nodes[i]["downloadlist"]=[]
    nodes[i]["uploadlist"]=[]
    nodes[i]["peerarrivaltime"]=0
    nodes[i]["downloadspeed"]=0
    nodes[i]["uploadspeed"]=0


seednode=random.randint(0,numberofnodes)

hashdata=string.ascii_letters

for i in range(10):
    piece={"pieceid":random.choice(hashdata),"piecesize":0.1}
    nodes[seednode]["pieces"].append(piece)

nodes[seednode]["id"]=1
deletesizes=[]
times=[]

for i in range(50,200,10):
    sim=NetworkSimulation(topology=G,agent_type=randompeerfailure,states=nodes,
                         num_trials=1,max_time=i,logging_interval=1.0,environmentparams={"time":i})


    sim.run_simulation()

    if i in faileddict.keys():
        deletesizes.append(len(faileddict[i]))
    else:
        deletesizes.append(0)
    times.append(i)

plt.bar(times,deletesizes,width=5)
plt.xlabel('times')
plt.ylabel('Number of failures')
plt.savefig('bittorrentrandomfailures.png')