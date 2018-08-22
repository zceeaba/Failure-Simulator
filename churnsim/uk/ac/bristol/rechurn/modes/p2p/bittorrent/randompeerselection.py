from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
from nxsim import BaseNetworkAgent
import random
import string
import random
#from churnsim.uk.ac.bristol.rechurn.bittorrent.Peer import Peer
#from churnsim.uk.ac.bristol.rechurn.bittorrent.Seed import Seed

#https://web.njit.edu/~dingxn/papers/BT-JSAC.pdf
#https://pdfs.semanticscholar.org/c16b/76c591f911672daf785aa5f601baff4b2ce6.pdf
faileddict={}

class randompeerfailure(BaseNetworkAgent):
    def __init__(self,environment,agent_id=0,state=()):
        super().__init__(environment=environment,agent_id=agent_id,state=state)
        self.datauploadmin=1000
        self.bite_prob=0.25
        self.hashdata=string.ascii_letters
        self.environment=environment
        self.time=environment.environment_params["environmentparams"]["time"]


    def autopopulate(self,data,span):
        speed=len(data)/span
        return speed

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
        currenttime=self.env.now
        totaltime=self.time
        deletednodes = []
        for i in all_neighbors:
            if currenttime==(self.time)/2 and i.state['downloadspeed']==0 and i.state["uploadspeed"]==0:
                deletednodes.append(i)
                faileddict[self.time]=deletednodes


        normal_neighbors = self.get_neighboring_agents(state_id=0)
        all_neighbors=self.get_all_agents()

        for neighbor in normal_neighbors:
            if random.random() < self.bite_prob:
                neighbor.state['id'] = 1 # zombie
                self.breakpiecesize(neighbor,all_neighbors,currenttime)
                print(self.env.now, self.id, neighbor.id, sep='\t')
                break

    def breakpiecesize(self,neighbor,all_neighbors,currentime):
        seedlist=[]
        for i in all_neighbors:
            if i.state['id']==1 and len(i.state['pieces'])>0:
                seedlist.append(i)

        if len(seedlist)>1:
            rdindex=random.randint(0,(len(seedlist)-1))
            #print(rdindex)
            self.makealink(neighbor,seedlist[rdindex],currentime)
        else:
            self.makealink(neighbor,seedlist[0],currentime)


    def makealink(self,to_node,from_node,currenttime):
        from_node.state["uploadlist"].append(to_node.state["peerid"])
        to_node.state["downloadlist"].append(from_node.state["peerid"])
        if currenttime>0:
            to_timespan=currenttime-to_node.state["peerarrivaltime"]
            to_node.state["downloadspeed"]=self.autopopulate(to_node.state["downloadlist"],to_timespan)
            from_timespan=currenttime-from_node.state["peerarrivaltime"]
            from_node.state["uploadspeed"]=self.autopopulate(from_node.state["uploadlist"],from_timespan)
        else:
            to_node.state["peerarrivaltime"]=currenttime
            from_node.state["peerarrivaltime"]=currenttime

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









