from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
from nxsim import BaseNetworkAgent
import random

class randompeerfailure(BaseNetworkAgent):
    def __init__(self,environment,agent_id=0,state=()):
        super().__init__(environment=environment,agent_id=agent_id,state=state)
        self.datauploadmin=1000
        self.bite_prob=0.25

    def run(self):
        while True:
            print("one iteration")
            if self.state['piecesize']==1:
                self.startmessaging()
                yield self.env.timeout(1)
            else:
                yield self.env.event()

    def startmessaging(self):
        normal_neighbors = self.get_neighboring_agents(state_id=0)
        for neighbor in normal_neighbors:
            if random.random() < self.bite_prob:
                neighbor.state['id'] = 1 # zombie
                print(self.env.now, self.id, neighbor.id, sep='\t')
                break

    #def







