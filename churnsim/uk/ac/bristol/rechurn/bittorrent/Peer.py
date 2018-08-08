class Peer:
    def __init__(self,config,id,init_pieces,up_bandwidth):
        self.conf=config
        self.id=id
        self.pieces=init_pieces
        self.up_bandwidth=up_bandwidth
        self.max_requests = self.conf.max_up_bw / self.conf.blocks_per_piece + 1
        self.max_requests = min(self.max_requests, self.conf.num_pieces)

    def requests(self, peers, history):
        return []

    def uploads(self, requests, peers, history):
        return []

    def downloads(self):
        return []