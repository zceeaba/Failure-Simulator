#https://www.liquidweb.com/blog/three-top-causes-cloud-outage/

import random
import socket
from threading import Thread
from collections import OrderedDict

class GossipNode:
    infected_nodes = []

    def __init__(self,id,capacity,host=None,port=None):
        self.id=id
        self.host=host
        self.port=port
        self.connected_nodes=[]
        self.sock=None
        self.tasklist=OrderedDict()
        self.capacity=capacity
        self.failure=0
        self.latestaddtime=0

    def connect_to_socket(self):
        sock=socket.socket()
        self.sock=sock
        self.sock.bind((self.host,self.port))
        self.sock.listen()

    def full(self,queue):
        reachedmaximum=False
        if len(queue.keys())==4:
            reachedmaximum=True

        return reachedmaximum

    def checksum(self,tasks,currenttime):
        if currenttime>0:
            spannedtime=currenttime-self.latestaddtime
        else:
            spannedtime=1
        workloadsum=0
        for i in tasks:
            workloadsum+=i
        tw=(workloadsum/self.capacity)
        if tw>spannedtime:
            self.failure=1
        else:
            self.failure=0
            self.latestaddtime=currenttime

    def assigntask(self,newtask,currenttime):
        if self.full(self.tasklist):
            popelement=list(self.tasklist.keys())[0]
            del self.tasklist[popelement]
        newdict=dict(self.tasklist)
        newdict[newtask.value]=newtask.taskid
        self.tasklist=OrderedDict(sorted(newdict.items()))
        self.checksum(self.tasklist,currenttime)

def try_gossip(nodes):
    for node in nodes:
        try:
            Thread(target=node.connect_to_socket()).start()
        except:
            print(node.host)
            print("Can't locate node"+str(node.host))




