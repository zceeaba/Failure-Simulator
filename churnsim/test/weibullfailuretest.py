from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.DiskFailures import weibullfailures
import networkx as nx
import matplotlib.pyplot as plt

wb=weibullfailures(True)
top = Topology()
#testnodejson=top.load_from_json()
failurelist = []

listofsizes=[i for i in range(10,1000,10)]
for i in listofsizes:
    testnodejson=nx.cycle_graph(i)
    failurelist.append(wb.get_new_topology(testnodejson))
print(failurelist)

plt.plot(listofsizes,failurelist)
plt.xlabel('number of nodes in graph')
plt.ylabel('number of failures')
plt.legend('')
plt.show()