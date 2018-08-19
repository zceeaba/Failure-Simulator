from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.software import SoftwareFailures
top = Topology()
testnodejson=top.load_from_json()
soft_failure = SoftwareFailures()
failed_top = soft_failure.get_new_topology(top)
