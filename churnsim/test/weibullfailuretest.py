from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.weibull import weibullfailures

wb=weibullfailures(True)
top = Topology()
testnodejson=top.load_from_json()

failurelist=wb.get_new_topology(top)
print(failurelist)
