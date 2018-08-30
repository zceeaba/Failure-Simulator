from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.Node import Node
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.Key import Key
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.Ring import Ring
from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.Fingers import Fingers



import numpy as np
import random
import networkx as nx
from matplotlib import pyplot as plt
import string
import random
random.seed(50)


##https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf


class ChordFailures(FailureMode):
    def __init__(self,time):
        self.time=time

    def id_generator(self,size=6, chars=string.ascii_uppercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def ip_generator(self,start_ip,end_ip):
        start = list(map(int, start_ip.split(".")))
        end = list(map(int, end_ip.split(".")))
        temp = start
        listofips = []

        listofips.append(start_ip)

        while temp != end:
            start[3] += 1
            for i in (3, 2, 1):
                if temp[i] == 256:
                    temp[i] = 0
                    temp[i - 1] += 1
            listofips.append(".".join(map(str, temp)))

        return listofips

    def draw_topology(self,topology):
        pos = nx.spring_layout(topology)
        nx.draw(topology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
        plt.show()

    def startiterativesearch(self,key,node):
        foundnode=None
        print(key)
        while node.Nodeid<key.id:
            fingertable=node.fingertable
            if fingertable[1] == 0:
                foundnode = None
                break
            if node.Nodeid>=key.id:
                foundnode=node
                break
            for i in fingertable:
                if fingertable[i].Nodeid>=key.id:
                    foundnode=fingertable[i]
                    break

            if foundnode:
                break
            else:
                length=len(node.fingertable.keys())
                node=node.fingertable[length]


        return foundnode

    def lookuperrors(self,ring):
        t=0
        foundcount=0
        while(t<self.time):
            keys=ring.keyslist
            chosenkey=random.choice(keys)
            node=ring.ringorder[0]
            failurenode=random.choice(ring.nodeslist)
            ring.nodeslist.remove(failurenode)

            ring.ringordering()
            foundnode=self.startiterativesearch(chosenkey,node)
            if foundnode is None:
                foundnode =ring.ringorder[0]

            if chosenkey in foundnode.keyslist:
                foundcount+=1
            else:
                print("not found",chosenkey.id)
            t+=1

        return foundcount




    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))

        new_topology = topology.copy()
        to_be_deleted = []

        keys=[self.id_generator() for i in range(0,30)]
        nodes=self.ip_generator("192.168.1.0", "192.168.1.30")

        ring=Ring()

        for node in nodes:
            newNode=Node(node)
            ring.nodejoin(newNode)

        ring.ringordering()
        ring.createsuccesors()

        for node in ring.nodeslist:
            finger=Fingers(3)
            if node.getsuccesor() is not None:
                finger.generatefinger(node)
            else:
                node.assignsuccesor(ring.ringorder[0])
                node.fingertable[1]=0
                node.fingertable[2]=0
                node.fingertable[3]=0

        for key in keys:
            newkey=Key(key)
            ring.keyadd(newkey)

        foundcount=self.lookuperrors(ring)

        return foundcount







