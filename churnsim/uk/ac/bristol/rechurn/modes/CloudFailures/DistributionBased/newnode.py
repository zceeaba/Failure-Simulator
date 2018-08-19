#from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.Gossip import GossipNode,try_gossip
from collections import OrderedDict
od=OrderedDict()
od[3]=5
od[4]=6
od[2]=8
newdict=dict(od)
newdict[7]=3
od=OrderedDict(sorted(newdict.items()))
print(od)
