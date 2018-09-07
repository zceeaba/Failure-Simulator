import collections
import random
import simpy
import networkx as nx
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.NetworkFailures.graph_methods import GraphSolve
import matplotlib.pyplot as plt
import os
import random


#http://iptps06.cs.ucsb.edu/papers/Guha-skype06.pdf
#https://www.globus.org/sites/default/files/gnutella.01.pdf
#Characterizing Churn in Gnutella Network in a New Aspect
#https://pdfs.semanticscholar.org/presentation/5b69/f772d9185860f2dc97661e90c275fed3582c.pdf
#http://people.cs.uchicago.edu/~matei/PAPERS/gnutella-rc.pdf
#https://ieeexplore.ieee.org/document/730882/
#https://www.backblaze.com/b2/hard-drive-test-data.html


RANDOM_SEED = 42
#peers = 50  # Number of tickets per movie
times =[i for i in range(50,500,50)]   # Simulate until
faillist=[]

class UniqueDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, value)
        else:
            raise KeyError("Key already exists")


def sessionlengthfailure(env,currenttime,peer,bandwidth,gnutella,SIM_TIME):
    with gnutella.counter.request() as peer_turn:
        result= yield peer_turn| gnutella.failed[peer]
        if peer_turn not in result:
            env.exit()

        gnutella.downtime[peer]+=(env.now-gnutella.start_time[peer])

        if gnutella.downtime[peer]>SIM_TIME/2:
            gnutella.num_failures[peer]+=1
            gnutella.num_failures[peer]+=len(gnutella.available[peer])

        yield env.timeout(1)



def peerarrivals(env,gnutella,SIM_TIME):
    while True:
        yield env.timeout(1)

        peer=random.choice(list(gnutella.peers))
        bandwidth=random.randint(1,6)

        currenttime = env.now
        if gnutella.peerenter[peer]==0:
            gnutella.start_time[peer]=currenttime

        gnutella.peerenter[peer]+=1


        if gnutella.start_time[peer]<SIM_TIME/2 and gnutella.available[peer]:
            env.process(sessionlengthfailure(env,currenttime,peer,bandwidth,gnutella,SIM_TIME))





def decision(probability):
    return random.random() < probability

cwdir = os.getcwd()

####Enter inputs for device placements
###Specify number of device nodes

sizes=[i for i in range(30,100,10)]
totalcountlist=[]
failurecountlist=[]

#for size in sizes:
#total_nodes = int(input("Enter total number of devices: "))
total_nodes=100

default_edge = int(0.6*total_nodes)
default_fog = int(total_nodes-default_edge)

#no_edge_nodes = int(input("Enter the number of edge nodes [Default=60% of total devices]: ") or default_edge)
#no_fog_nodes = int(input("Enter the number of fog nodes [Default=40% of total devices]: ") or default_fog)
no_edge_nodes=default_edge
no_fog_nodes=default_fog

##Specify probabilities for network connections
#print("#### Enter the network densities between the devices ####")
#prob_edge = float(input("Enter connections density between edge nodes (0-1) [Default=0.2]: ") or "0.2")
#prob_fog = float(input("Enter connections density between fog nodes (0-1) [Default=0.6]: ") or "0.6")
#prob_edge_fog = float(input("Enter connections density between edge and fog nodes (0-1) [Default=0.5]: ") or "0.5")
prob_edge=0.2
prob_fog=0.6
prob_edge_fog=0.5

##Create an empty graph
G = nx.Graph()  # Graph for devices

edge_nodes = list(range(0, no_edge_nodes))
fog_nodes = list(range(no_edge_nodes, total_nodes))

##Add Device nodes to graph
for i in enumerate(edge_nodes):
    G.add_node(i[1], type="edge", name=i[1],trafficin=0,trafficout=0,demand_value=0)

for i in enumerate(fog_nodes):
    G.add_node(i[1], type="fog", name=i[1],trafficin=0,trafficout=0,demand_value=0)


##Connections between the edge
for i in range(len(edge_nodes)):
    j = i + 1
    while j < len(edge_nodes):
        choice = decision(prob_edge)
        if choice == True:
            G.add_edge(edge_nodes[i], edge_nodes[j], weight=random.randint(1, 2))
        j = j + 1

##Connections between the fog
for i in range(len(fog_nodes)):
    j = i + 1
    while j < len(fog_nodes):
        choice = decision(prob_fog)
        if choice == True:
            G.add_edge(fog_nodes[i], fog_nodes[j], weight=random.randint(1, 2))
        j = j + 1

# Connections between the edge and fog
lastCount = 0
for i in range(len(edge_nodes)):
    alreadyConnected = False
    for j in range(len(fog_nodes)):
        lastCount = lastCount + 1
        choice = decision(prob_edge_fog)
        if choice == True:
            G.add_edge(edge_nodes[i], fog_nodes[j], weight=random.randint(2, 5))
            alreadyConnected = True
        if (lastCount == len(
                fog_nodes) - 1 and alreadyConnected == False):  # to ensure that edge node is connected to atleast one fog node
            randomNode = random.randint(0, len(fog_nodes) - 1)
            G.add_edge(edge_nodes[i], fog_nodes[randomNode], weight=random.randint(2, 5))

edgedevices=[]
fogdevices=[]
for x in G._node:
    if G.node[x]['type']=="edge":
        edgedevices.append(x)
    else:
        fogdevices.append(x)

total_nodes=len(edgedevices)+len(fogdevices)

for x in G:
    neighbors = [n for n in G.neighbors(x)]
    if G.node[x]["type"]=="fog":
        trafficin,trafficout=0,0
        for y in neighbors:
            if G.node[y]["type"]=="edge":
                trafficin+=1
            elif G.node[y]["type"]=="fog":
                trafficout+=1
        G.node[x]["trafficin"]=trafficin
        G.node[x]["trafficout"]=trafficout
    elif G.node[x]["type"]=="edge":
        trafficin,trafficout=0,0
        for y in neighbors:
            if G.node[y]["type"]=="fog":
                trafficout+=1
            elif G.node[y]["type"]=="edge":
                trafficin+=1
        G.node[x]["trafficin"]=trafficin
        G.node[x]["trafficout"]=trafficout

demands_matrix={}
for i in range(total_nodes):
    for j in range(total_nodes):
        if i==j:
            continue
        else:
            if (G.node[i]["trafficin"] + G.node[j]["trafficin"])==0:
                demand_value=0
            else:
                demand_value=(G.node[i]["trafficout"]+G.node[j]["trafficout"])/(G.node[i]["trafficin"]+G.node[j]["trafficin"])
            demands_matrix.update({(i, j): demand_value})
path=[]
failurecount=0
totalcount=0
for i in range(total_nodes):
    for j in range(total_nodes):
        if i==j:
            continue
        else:
            path=nx.dijkstra_path_length(G,i,j,weight="weight")
            capacity=path
            if capacity<demands_matrix[(i,j)]:
                failurecount+=1
            totalcount+=1

totalcountlist.append(totalcount)
failurecountlist.append(failurecount)

print(totalcountlist)
print(failurecountlist)

#plt.plot(totalcountlist,failurecountlist)
#plt.ylabel('number of failures')
#plt.xlabel('Size of network')
#plt.savefig('networkfailuresiot.png')


for time in times:
    SIM_TIME=time

    g=G.copy()

    cg=None
    for sg in nx.connected_component_subgraphs(g):
        if cg==None or len(sg.nodes())>len(cg.nodes()):
            cg=sg

    Gnutella=collections.namedtuple('Gnutella', 'counter, peers, available, '
                                                'failed, when_failed, '
                                                'num_failures,failurescore,start_time,downtime,peerenter')

    random.seed(RANDOM_SEED)
    env=simpy.Environment()
    counter = simpy.Resource(env, capacity=1)

    peers=cg.nodes
    edges=cg.edges
    available=UniqueDict()

    for peer in peers:
        available[peer]=[]

    for x,y in edges:
        typea=G.node[y]["type"]
        typeb=G.node[x]["type"]
        if typea=="edge" and typeb=="edge":
            available[x].append(y)




    peerenter={peer:0 for peer in peers}
    start_time={peer:0 for peer in peers}

    downtime={peer:0 for peer in peers}

    failed={peer:env.event() for peer in peers}
    when_failed={peer:None for peer in peers}
    num_failures={peer:0 for peer in peers}
    failurescore={peer:1 for peer in peers}

    gnutella = Gnutella(counter, peers, available, failed, when_failed,
                      num_failures,failurescore,start_time,downtime,peerenter)


    env.process(peerarrivals(env, gnutella,SIM_TIME))
    env.run(until=SIM_TIME)


    sum=0
    for peer in peers:
        sum+=gnutella.num_failures[peer]

    faillist.append(sum)

print(len(G.edges))
print(faillist)
newfaillist=[]
for i in range(len(faillist)):
    newfaillist.append(failurecountlist[0]+faillist[i])
plt.plot(times,faillist)
plt.plot(times,newfaillist)
plt.xlabel('total simulation time')
plt.ylabel('number of failures')
plt.savefig('gnutellaiotfailures.png')
