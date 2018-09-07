from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.DiskFailures import weibullfailures
import networkx as nx
import matplotlib.pyplot as plt


top = Topology()
#testnodejson=top.load_from_json()
failurelist = []

listofsizes=[500]
times=[i for i in range(50,750,50)]
#times=[30]
for time in times:
    wb = weibullfailures(True,time/10)
    testnodejson=nx.path_graph(listofsizes[0])
    failurelist.append(wb.get_new_topology(testnodejson))
print(failurelist)

failureratio=[]
for i in range(len(times)):
    failureratio.append(failurelist[i]/times[i])

print(failureratio)
#plt.plot(listofsizes,failurelist)
sum=0
plt.scatter(times,failureratio)
for i in failureratio:
    sum+=i
meanvalue=sum/len(failureratio)
print(meanvalue)
plt.xlabel('time')
plt.ylabel('Rate of failure')
plt.show()
