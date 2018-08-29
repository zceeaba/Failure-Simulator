class Fingers:
    def __init__(self,size):
        self.m=size

    def generatefinger(self,node):
        i=1
        tempnode=node
        while(i<self.m):
            succesor=tempnode.getsuccesor()
            while(succesor is not None):
                sumvalue = node.Nodeid + 2 ** (i-1)
                if succesor.Nodeid>sumvalue:
                    node.fingertable[i]=succesor
                    i=i+1
                else:
                    tempnode=succesor
                    break

        print(node)
