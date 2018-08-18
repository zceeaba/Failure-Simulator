from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.DataBasedFailures.software import softwarefailure
top = Topology()
testnodejson=top.load_from_google()
soft_failure = softwarefailure()
failed_top = soft_failure.get_new_topology(top)
#self.assertTrue(len(failed_top.nodes) < len(top.nodes))
