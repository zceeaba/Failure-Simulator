from churnsim.uk.ac.bristol.rechurn.topology import Topology
from churnsim.uk.ac.bristol.rechurn.modes.SelectionBasedFailures.random_mode import RandomFailures
import unittest

class TestRandomFailure(unittest.TestCase):

    def test_random(self):
        top = Topology()
        loaded = top.load_from_csvs('../nodes.csv','../edges.csv')
        #loaded=top.load_from_google()
        self.assertTrue(loaded)
        random_failure = RandomFailures()
        failed_top = random_failure.get_new_topology(top)
        self.assertTrue(len(failed_top.nodes)<len(top.nodes))


if __name__ == '__main__':
    unittest.main()