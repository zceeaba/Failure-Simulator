from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
from nxsim import BaseNetworkAgent
import random
import string
import random
#from churnsim.uk.ac.bristol.rechurn.bittorrent.Peer import Peer
#from churnsim.uk.ac.bristol.rechurn.bittorrent.Seed import Seed

class randompeerfailure(BaseNetworkAgent):
    def __init__(self,environment,agent_id=0,state=()):
        super().__init__(environment=environment,agent_id=agent_id,state=state)
        self.datauploadmin=1000
        self.bite_prob=0.25
        self.hashdata=string.ascii_letters

    def run(self):
        while True:
            print("one iteration")
            if self.state['id']==1:
                self.startmessaging()
                yield self.env.timeout(1)
            else:
                yield self.env.event()

    def sethashdata(self,hashdata):
        self.hashdata=hashdata

    def startmessaging(self):
        normal_neighbors = self.get_neighboring_agents(state_id=0)
        all_neighbors=self.get_all_agents()
        for neighbor in normal_neighbors:
            if random.random() < self.bite_prob:
                neighbor.state['id'] = 1 # zombie
                self.breakpiecesize(neighbor,all_neighbors)
                print(self.env.now, self.id, neighbor.id, sep='\t')
                break

    def breakpiecesize(self,neighbor,all_neighbors):
        seedlist=[]
        for i in all_neighbors:
            if i.state['id']==1 and len(i.state['pieces'])>0:
                seedlist.append(i)
        if len(seedlist)>1:
            rdindex=random.randint(0,(len(seedlist)-1))
            print(rdindex)
            self.makealink(neighbor,seedlist[rdindex])
        else:
            self.makealink(neighbor,seedlist[0])


    def makealink(self,to_node,from_node):
        from_node.state["uploadlist"].append(to_node.state["peerid"])
        to_node.state["downloadlist"].append(from_node.state["peerid"])
        frompieces=from_node.state["pieces"]
        topieces=to_node.state["pieces"]
        chosenpeer={}
        for i in frompieces:
            if i in topieces:
                continue
            else:
                chosenpeer=i
                break


        to_node.state["pieces"].append(chosenpeer)
        print("addition")








