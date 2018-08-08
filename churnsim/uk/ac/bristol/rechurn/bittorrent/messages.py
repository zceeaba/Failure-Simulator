class Request:
    def __init__(self,requester_id,peer_id,piece_id,start):
        self.requester_id=requester_id
        self.peer_id=peer_id
        self.piece_id=piece_id
        self.start=start

class Upload:
    def __init__(self,from_id,to_id,up_bw):
        self.from_id=from_id
        self.to_id=to_id
        self.up_bw=up_bw

class Download:
    def __init__(self,from_id,to_id,piece,blocks):
        self.from_id=from_id
        self.to_id=to_id
        self.piece=piece
        self.blocks=blocks
