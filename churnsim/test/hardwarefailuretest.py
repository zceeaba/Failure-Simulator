from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.DataBasedFailures.hardware import hardwarefailure
top = Topology()
testnodejson=top.load_from_json()
hard_failure = hardwarefailure()
failed_top = hard_failure.get_new_topology(top)
#self.assertTrue(len(failed_top.nodes) < len(top.nodes))
