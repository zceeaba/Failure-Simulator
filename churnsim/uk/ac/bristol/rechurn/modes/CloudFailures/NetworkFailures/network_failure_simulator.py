#http://conferences.sigcomm.org/sigcomm/2011/papers/sigcomm/p350.pdf
#https://arxiv.org/ftp/arxiv/papers/1608/1608.03770.pdf
#https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41315.pdf
#https://github.com/subinjp/edgecomputing/blob/master/pdfs/A_Survey_on_Mobile_Edge_Computing.pdf
#https://www.isi.edu/~johnh/PAPERS/Heidemann18b.pdf
#https://www.researchgate.net/publication/224504245_Graph-Based_P2P_Traffic_Classification_at_the_Internet_Backbone

from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
import re
import itertools
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.NetworkFailures import graph_methods

def generatecombinations(data):
	comblist=[]
	for i in data:
		for j in data:
			for k in data:
				newtuple=(i,j,k)
				comblist.append(newtuple)

	return comblist

G = nx.DiGraph() #Create an empty graph with no nodes and no edges.
TR_OUT=[i for i in range(10,40,10)]
combtrout=generatecombinations(TR_OUT)

#for subset in itertools.combinations(TR_OUT,3):
#	combtrout.append(subset)


numberdeleted=[]
tf=0
while tf<len(combtrout):
	links_file = open('links.txt', "r")  # specify location of the links file
	for line in links_file:
		line = line.strip()
		orig,dest,dist=line.split(",")
		G.add_edge(orig,dest,weight=int(dist)) #add links to the graph by parsing contents of the links.txt file
	links_file.close()
	nodes = G.nodes()
	links = G.edges()
	result_file = open('wc_results.txt',"w")
	#print(result_file, "Created graph with the following nodes:")
	pprint(nodes,result_file)
	#print(result_file, "Created graph with the following links:")
	pprint(links,result_file)

	#plt.savefig('topology_result.png')
	x = graph_methods.GraphSolve() #create a new instance of a class
	autotraffic=combtrout[tf]
	print(autotraffic)
	tf=tf+1
	flows = x.Gravity('pe_traffic.txt',autotraffic) #generate demands file from pe traffic
	print(result_file, "Generated the following demands from PE traffic:")
	pprint (flows)

	wc_link_util = {} # list containing node_a - node_b link tuples and traffic levels for every failure
	links=list(links)
	#nx.draw(G)
	#plt.show()

	newtopology=G.copy()
	deletelist=[]
	pos = nx.spring_layout(newtopology)

	for link in links:
		link_to_remove_1 = (link[0], link[1])
		link_to_remove_2 = (link[1], link[0])
		links.remove(link_to_remove_2)
		G.remove_edge(*link_to_remove_1)
		G.remove_edge(*link_to_remove_2)
		wc_link_util.update({link_to_remove_1:x.Flows_to_Loads(flows,G)})
		G.add_edge(*link_to_remove_1)
		G.add_edge(*link_to_remove_2)
		print(link_to_remove_1,link_to_remove_2)
		#if wc_link_util[link_to_remove_1][]
		for i in wc_link_util[link_to_remove_1]:
			if wc_link_util[link_to_remove_1][i]>=10 and (i not in deletelist):
				newtopology.remove_edge(*i)
				deletelist.append(i)
		#nx.draw(newtopology, pos, with_labels=True, arrows=True, node_size=1000)  # generic graph layout
		#plt.show()

	wc_util = x.Worst_Case_Util(wc_link_util)

#pprint(wc_util)
#print(result_file, "Worst case link utilisations:")
#pprint (wc_util,result_file)

#pprint (wc_link_util)

#pprint(len(deletelist))
	numberdeleted.append(len(deletelist))

"""
combtroutxindices=[i[0] for i in combtrout]
combtroutyindices=[i[1] for i in combtrout]
combtroutzindices=[i[2] for i in combtrout]
plt.scatter(numberdeleted,combtroutxindices)
plt.scatter(numberdeleted,combtroutyindices)
plt.scatter(numberdeleted,combtroutzindices)
"""
combtroutindices=[i for i in range(len(combtrout))]
plt.scatter(combtroutindices,numberdeleted)
plt.xlabel('Configuration mode')
plt.ylabel('Number of links failed')
plt.savefig('network.png')

print(combtrout)
