import collections
import random
import simpy
import networkx as nx

#http://iptps06.cs.ucsb.edu/papers/Guha-skype06.pdf

RANDOM_SEED = 42
#peers = 50  # Number of tickets per movie
SIM_TIME = 100000  # Simulate until

def sessionlengthfailure(env,peer,bandwidth,gnutella):
    with gnutella.counter.request() as peer_turn:
        result= yield peer_turn| gnutella.failed[peer]
        # Check if it's our turn of if movie is sold out
        if peer_turn not in result:
            gnutella.num_failures[peer] += 1
            env.exit()

        # Check if enough tickets left.

        if gnutella.available[peer] < bandwidth:
            # Moviegoer leaves after some discussion
            yield env.timeout(0.5)
            env.exit()


        # Buy tickets
        gnutella.available[peer] -= bandwidth

        if gnutella.available[peer] < 2:
            # Trigger the "sold out" event for the movie
            gnutella.failed[peer].succeed()
            gnutella.when_failed[peer] = env.now
            gnutella.available[peer] = 0
        yield env.timeout(1)



def peerarrivals(env,gnutella):
    while True:
        yield env.timeout(random.expovariate(1/0.5))

        peer=random.choice(list(gnutella.peers))
        bandwidth=random.randint(1,6)
        #print(gnutella.available[peer])
        if gnutella.available[peer]:
            env.process(sessionlengthfailure(env,peer,bandwidth,gnutella))




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
                                            'num_failures')

random.seed(RANDOM_SEED)
env=simpy.Environment()
counter = simpy.Resource(env, capacity=1)

peers=cg.nodes
available={peer:10 for peer in peers}
failed={peer:env.event() for peer in peers}
when_failed={peer:None for peer in peers}
num_failures={peer:0 for peer in peers}

gnutella = Gnutella(counter, peers, available, failed, when_failed,
                  num_failures)



print(peers)
env.process(peerarrivals(env, gnutella))
env.run(until=SIM_TIME)

for peer in peers:
    if gnutella.failed[peer] and gnutella.when_failed[peer]:
        print('Peer "%s" failed out %.1f minutes after ticket counter '
              'opening.' % (peer, gnutella.when_failed[peer]))
        print('  Number of peers leaving queue when peer failed: %s' %
              gnutella.num_failures[peer])

