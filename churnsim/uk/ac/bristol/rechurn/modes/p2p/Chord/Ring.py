class Ring:
    def __init__(self):
        self.nodeslist=[]

    def nodejoin(self,node):
        self.nodeslist.append(node)
        self.updaterouting()

    def nodeleave(self,node):
        self.nodeslist.pop()

    def updaterouting(self):
        print("to do")