from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.hash import chord_hash
class Node:
    def __init__(self,Nodestring):
        self.Nodeid=chord_hash(Nodestring)#identifier length m large enough so that identifiers can't be the same
        self.fingertable={}
        self.keyslist=[]
        self.succesor=None

    def addkey(self,key):
        self.keyslist.append(key)

    def assignsuccesor(self,succesor):
        self.succesor=succesor

    def getsuccesor(self):
        return self.succesor

