from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.hash import chord_hash
class Node:
    def __init__(self,Nodestring):
        self.Nodeid=chord_hash(Nodestring)#identifier length m large enough so that identifiers can't be the same