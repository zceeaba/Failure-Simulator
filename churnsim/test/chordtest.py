from churnsim.uk.ac.bristol.rechurn.modes.p2p.Chord.chord import ChordFailures
from churnsim.uk.ac.bristol.rechurn.topology import Topology
from matplotlib import pyplot as plt

top = Topology()
time=[i for i in range(30,200,10)]
failurelist=[]
for i in time:
    chordfailure=ChordFailures(i)
    failed_chord = chordfailure.get_new_topology(top)
    failurelist.append(failed_chord)

plt.bar(time,failurelist)
plt.xlabel('iterations')
plt.ylabel('number of failures')
plt.savefig('lookuperrorchord.png')

