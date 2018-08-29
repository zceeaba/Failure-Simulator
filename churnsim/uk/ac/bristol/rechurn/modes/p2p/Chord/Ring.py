from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.twowaydict import TwoWayDict
import collections

class Ring:
    def __init__(self):
        self.nodeslist=[]
        self.keyslist=[]
        self.ringorder=collections.OrderedDict()
    def nodejoin(self,node):
        self.nodeslist.append(node)
        #self.updateroutingtable(node)

    def keyadd(self,key):
        self.keyslist.append(key)
        self.updatenode(key)

    def nodeleave(self,node):
        self.nodeslist.pop()

    def findnearest(self,nodes,key):
        Minimum=0
        for i in range(len(nodes)):
            currentnodeid=nodes[i].Nodeid
            minimumnodeid=nodes[Minimum].Nodeid
            keyid=key.id
            diff=currentnodeid-keyid
            Minimumdiff=minimumnodeid-keyid
            if diff>=0 and diff<abs(Minimumdiff):
                Minimum=i

        return Minimum

    def updatenode(self,key):
        nodes=self.nodeslist
        loc=self.findnearest(nodes,key)
        key.assignsuccesor(nodes[loc])
        nodes[loc].addkey(key)

    def ringordering(self):
        templist=[]
        for i in self.nodeslist:
            templist.append(i.Nodeid)

        templist=sorted(templist)

        for k in range(len(templist)):
            for j in range(len(self.nodeslist)):
                temp=templist[k]
                node=self.nodeslist[j]
                nodeid=node.Nodeid
                if temp==nodeid:
                    self.ringorder[k]=node


    def createsuccesors(self):
        for i in range(len(self.ringorder.keys())):
            succesorpos=i+1
            node=self.ringorder[i]
            if succesorpos<len(self.ringorder.keys()):
                succesornode=self.ringorder[succesorpos]
                node.assignsuccesor(succesornode)








