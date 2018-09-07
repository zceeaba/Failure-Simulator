from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.DiskFailures import weibullfailures
import networkx as nx
import matplotlib.pyplot as plt

wb=weibullfailures(True)
top = Topology()
#testnodejson=top.load_from_json()
failurelist = []
