from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.chord import ChordFailures
from churnsim.uk.ac.bristol.rechurn.topology import Topology

top = Topology()

chordfailure=ChordFailures()
failed_chord = chordfailure.get_new_topology(top)
