from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.hash import chord_hash
class key:
    def __init__(self,keystring,predecessor=None,successor=None):
        self.id=chord_hash(keystring)
        self.predecessor=predecessor
        self.successor=successor
        self.nodelist=[]

    def assignsuccesor(self,succesor):
        self.successor=succesor

    def assignpredecessor(self,predecessor):
        self.predecessor=predecessor

    def addnode(self,node):
        self.nodelist.append(node)

