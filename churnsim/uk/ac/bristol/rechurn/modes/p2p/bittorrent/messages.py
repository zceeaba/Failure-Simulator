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
