from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.SoftwareFailures.software import SoftwareFailures
import networkx as nx
#top = Topology()
#testnodejson=top.load_from_json()
top=nx.path_graph(100)
soft_failure = SoftwareFailures()
failed_top = soft_failure.get_new_topology(top)
