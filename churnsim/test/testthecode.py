from churnsim.uk.ac.bristol.rechurn.topology import Topology

top = Topology()
googlenode=top.load_from_google()
#testnodejson=top.load_from_json()
#loaded = top.load_from_csvs('../nodes.csv', '../edges.csv')
#nat_failure = RandomFailures()
#failed_top = nat_failure.get_new_topology(top)
#self.assertTrue(len(failed_top.nodes) < len(top.nodes))
