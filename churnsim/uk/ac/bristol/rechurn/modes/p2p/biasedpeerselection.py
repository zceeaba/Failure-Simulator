#http://conferences.sigcomm.org/imc/2006/papers/p19-stutzbach2.pdf
from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
from nxsim import BaseNetworkAgent

class biasedpeerfailure(BaseNetworkAgent):
    def __init__(self,environment,agent_id=0,state=()):
        super().__init__(environment=environment,agent_id=agent_id,state=state)
        self.datauploadmin=1000

    def run(self):
        while True:
            if self.state['failure']==1:
                self.generatefailure()
                yield self.env.timeout(1)
            else:
                yield self.env.event()

    def generatefailure(self):
        non_failure_nodes=self.get_neighboring_agents(state_id=0)
        connected_nodes=self.getcloselyconnectednodes(non_failure_nodes)

    def getcloselyconnectednodes(self,non_failure_nodes):
        meanbandwidth=self.computemeanbandwidth(non_failure_nodes)
        chosennodes=[]
        for i in non_failure_nodes:
            if non_failure_nodes["bandwidthlastttsecs"]>=meanbandwidth:
                chosennodes.append(i)

        connectednodes=chosennodes[:6]
        chooselastnode=self.biasedpeerselection(non_failure_nodes)

    def computemeanbandwidth(self,nodes):
        bdltt=[]
        for i in nodes:
            bdltt.append(nodes["bandwidthlastttsecs"])
        return sum(bdltt)/len(bdltt)

    def biasedpeerselection(self,non_failure_nodes):
        assignprobabilities=[i for i in range(0,75,7)]
        newdict=[]
        keys=range(non_failure_nodes)

        for i in keys:
            newdict[i]["node"]=non_failure_nodes[i]
            newdict[i]["probability"]=assignprobabilities[i]


        return True



