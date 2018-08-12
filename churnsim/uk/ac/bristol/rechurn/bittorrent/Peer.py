from churnsim.uk.ac.bristol.rechurn.bittorrent.messages import Upload,Download
class Peer:
    def __init__(self,id,init_pieces,up_bandwidth):
        #self.conf=config
        self.id=id
        self.pieces=[]
        #self.max_requests = (self.conf.max_up_bw / self.conf.blocks_per_piece) + 1
        #self.max_requests = min(self.max_requests, self.conf.num_pieces)
        self.requests=[]
        self.uploads=[]#
        self.downloads=[]

    def download(self,Pieceobject):
        self.pieces.append(Pieceobject)

    def makeupload(self,targetnodeid):
        newUpload(self.id,targetnodeid,)
        self.uploads.append()

    def requests(self, peers, history):
        return self.requests

    def uploads(self):
        return self.uploads

    def downloads(self):
        return self.downloads