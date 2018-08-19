from churnsim.uk.ac.bristol.rechurn.failure_mode import FailureMode
from churnsim.uk.ac.bristol.rechurn.topology import Topology
import numpy as np
from scipy.stats import expon
import networkx as nx
from collections import defaultdict

#http://delivery.acm.org/10.1145/2750000/2741964/a18-verma.pdf?ip=137.222.114.240&id=2741964&acc=TRUSTED&key=BF07A2EE685417C5%2E3DCFD3605FE4B4CE%2E4D4702B0C3E38B35%2EE47D41B086F0CDA3&__acm__=1532018289_f91b72ab8b3464dca2da2dfa31ad9766
#https://groups.google.com/forum/#!searchin/googleclusterdata-discuss/what$20is$20the$20job$20type%7Csort:date/googleclusterdata-discuss/sefBf16qVTY/DaFfGe4PDgAJ
#https://pdfs.semanticscholar.org/a07d/108bc9a274f9cbc7278c3ecab0816843fc91.pdf

class UniqueDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, value)
        else:
            raise KeyError("Key already exists")

class softwarefailure(FailureMode):
    def checkforfailures(self,jobdata):
        for x in jobdata:
            print(jobdata[x]["Time"])
            #timetaken=jobdata["Time"]
        #ts=workload/mips
        return True

    def get_new_topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('topology argument is not of type ' + type(topology))
        num_nodes=len(topology.nodes)


        deletenodes=[]

        #jobdict=UniqueDict.fromkeys(topology.nodes)
        keylist=list(set(topology.nodes))
        jobdict=dict.fromkeys(keylist)
        for i in jobdict.keys():
            jobdict[i]=[]

        for x in topology:
            jobdict[x].append(topology[x])

        count=0
        newdict={}
        for j in jobdict.keys():
            attributes=jobdict[j]
            #print(len(attributes[0]))
            if len(attributes[0])>1:
                count+=1
                newdict[j]=attributes
                self.checkforfailures(attributes[0])

                print(newdict)




        return topology

