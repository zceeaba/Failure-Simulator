class Piece:
    def __init__(self,size,id):
        self.size=size
        self.id=id
        self.owners=[]

    def addnewowner(self,node_id):
        self.owners.append(node_id)