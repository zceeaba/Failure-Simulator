import collections
import random
import simpy
import networkx as nx

#http://iptps06.cs.ucsb.edu/papers/Guha-skype06.pdf
#https://www.globus.org/sites/default/files/gnutella.01.pdf
#Characterizing Churn in Gnutella Network in a New Aspect


RANDOM_SEED = 42
#peers = 50  # Number of tickets per movie
SIM_TIME = 2000  # Simulate until

class UniqueDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, value)
        else:
            raise KeyError("Key already exists")


def sessionlengthfailure(env,currenttime,peer,bandwidth,gnutella):
    with gnutella.counter.request() as peer_turn:
        result= yield peer_turn| gnutella.failed[peer]
        if peer_turn not in result:
            env.exit()

        # Check if enough tickets left.
        """
        if gnutella.available[peer] < bandwidth:
            yield env.timeout(0.5)
            env.exit()
        """

        gnutella.downtime[peer]+=(env.now-gnutella.start_time[peer])

        if gnutella.downtime[peer]>SIM_TIME/2:
            gnutella.num_failures[peer]+=1
            gnutella.num_failures[peer]+=len(gnutella.available[peer])
        

        """
        if len(gnutella.available[peer]:
            # Trigger the peer failure event for the movie
            gnutella.failed[peer].succeed()
            gnutella.when_failed[peer] = env.now
            gnutella.available[peer] = 0
        """

        yield env.timeout(1)



def peerarrivals(env,gnutella):
    while True:
        yield env.timeout(random.expovariate(SIM_TIME/2))

        peer=random.choice(list(gnutella.peers))
        bandwidth=random.randint(1,6)

        currenttime = env.now
        if gnutella.peerenter[peer]==0:
            gnutella.start_time[peer]=currenttime

        gnutella.peerenter[peer]+=1


        if gnutella.start_time[peer]<SIM_TIME/2 and gnutella.available[peer]:
            env.process(sessionlengthfailure(env,currenttime,peer,bandwidth,gnutella))




import matplotlib.pyplot as plt
import numpy as np
import gzip
import urllib.request


def print_graph_stats(title, g):
    print("Simple stats for: " + title)
    print("# of nodes: " + str(len(g.nodes())))
    print("# of edges: " + str(len(g.edges())))
    print("Is graph connected? " + str(nx.is_connected(g)))


# Download file from SNAP and uncompress it.
response = urllib.request.urlopen('http://snap.stanford.edu/data/p2p-Gnutella09.txt.gz')
with open('p2p-Gnutella09.txt', 'wb') as outfile:
    outfile.write(gzip.decompress(response.read()))

g = nx.read_edgelist('p2p-Gnutella09.txt')
#print_graph_stats("Gnutella p2p graph", g)

cg=None
for sg in nx.connected_component_subgraphs(g):
    if cg==None or len(sg.nodes())>len(cg.nodes()):
        cg=sg

#print_graph_stats("Gnutella p2p graph",cg)
Gnutella=collections.namedtuple('Gnutella', 'counter, peers, available, '
                                            'failed, when_failed, '
                                            'num_failures,start_time,downtime,peerenter')

random.seed(RANDOM_SEED)
env=simpy.Environment()
counter = simpy.Resource(env, capacity=1)

peers=cg.nodes
edges=cg.edges
available=UniqueDict()

for peer in peers:
    available[peer]=[]

for x,y in edges:
    available[x].append(y)

peerenter={peer:0 for peer in peers}
start_time={peer:0 for peer in peers}

downtime={peer:0 for peer in peers}

failed={peer:env.event() for peer in peers}
when_failed={peer:None for peer in peers}
num_failures={peer:0 for peer in peers}

gnutella = Gnutella(counter, peers, available, failed, when_failed,
                  num_failures,start_time,downtime,peerenter)


env.process(peerarrivals(env, gnutella))
env.run(until=SIM_TIME)


sum=0
for peer in peers:
    sum+=gnutella.num_failures[peer]

print(len(peers)-sum)

""""
for peer in peers:
    if gnutella.failed[peer] and gnutella.when_failed[peer]:
        print('Peer "%s" failed out %.1f minutes after ticket counter '
              'opening.' % (peer, gnutella.when_failed[peer]))
        print('  Number of peers leaving loop when peer failed: %s' %
              gnutella.num_failures[peer])
        failednodes.append(gnutella.num_failures[peer])

sum=0
for i in failednodes:
    sum+=i

print(sum)
"""