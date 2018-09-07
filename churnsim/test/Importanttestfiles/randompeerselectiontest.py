from nxsim import NetworkSimulation
from churnsim.uk.ac.bristol.rechurn.modes.p2p.bittorrent.randompeerselection import randompeerfailure
from networkx import nx
import string
import random
from matplotlib import pyplot as plt

deletesizes = []
numberofnodes=200
times = [i for i in range(100,600,50)]
#piecesizes=[i for i in range(100,700,50)]
piecesizes=[i for i in range(100,600,50)]
for time in times:
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
        #piece={"pieceid":random.choice(hashdata),"piecesize":ps/20}
        piece = {"pieceid": random.choice(hashdata), "piecesize": 0.1}
        nodes[seednode]["pieces"].append(piece)

    nodes[seednode]["id"]=1

#for i in range(50,200,10):
    sim=NetworkSimulation(topology=G,agent_type=randompeerfailure,states=nodes,
                         num_trials=1,max_time=time,logging_interval=1.0,environmentparams={"time":time,"faileddict":{}})


    sim.run_simulation()
    faileddict=sim.environment_params["environmentparams"]["faileddict"]

    if time in faileddict.keys():
        deletesizes.append(len(faileddict[time]))
    else:
        deletesizes.append(0)

print(deletesizes,piecesizes)
failureratios=[]
for i in range(len(deletesizes)):
    #failureratios.append((deletesizes[i]/piecesizes[i]))
    failureratios.append(((200-deletesizes[i])))



plt.bar(piecesizes,failureratios,width=10)
plt.xlabel('time of running')
plt.ylabel('population')
plt.show()
