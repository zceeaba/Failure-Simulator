from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.SoftwareFailures.software import SoftwareFailures
import networkx as nx
from matplotlib import pyplot as plt

#https://www.slideshare.net/abhinavtheneo/chapter-7-software-reliability

#top = Topology()
#testnodejson=top.load_from_json()
times=[i for i in range(100,3000,100)]
top=nx.path_graph(1000)
numberfailures=[]

for i in times:
    soft_failure = SoftwareFailures(i)
    failed_top = soft_failure.get_new_topology(top)
    numberfailures.append(failed_top)

print(numberfailures)
failurerate=[]

for i in range(len(numberfailures)):
    failurerate.append(numberfailures[i]/times[i])

plt.plot(times,failurerate)
plt.xlabel('time')
plt.ylabel('failure rate')
plt.show()