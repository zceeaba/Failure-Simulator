from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
import re
from churnsim.uk.ac.bristol.rechurn.modes.network_simulator import graph_methods

G = nx.DiGraph() #Create an empty graph with no nodes and no edges.
links_file = open('links.txt',"r") #specify location of the links file
for line in links_file:
	line = line.strip()
	orig,dest,dist = line.split(",")
	G.add_edge(orig,dest,weight=int(dist)) #add links to the graph by parsing contents of the links.txt file
links_file.close()
nodes = G.nodes()
links = G.edges()
result_file = open('wc_results.txt',"w")
print(result_file, "Created graph with the following nodes:")
pprint(nodes,result_file)
print(result_file, "Created graph with the following links:")
pprint(links,result_file)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True,arrows=False,node_size=1000) #generic graph layout
nodelist = [x for x in nodes if re.search('pe[0-9]', x)] #create a list containing PE nodes only
nx.draw_networkx_nodes(G,pos,nodelist=nodelist,node_color='b',node_size=1000) # change PE node colour to blue
edge_labels=dict([((u,v,),d['weight']) #create a dictionary with edges and weights
             for u,v,d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels) # draw edge labels
plt.savefig('topology_result.png')

x = graph_methods.GraphSolve() #create a new instance of a class
flows = x.Gravity('pe_traffic.txt') #generate demands file from pe traffic
print(result_file, "Generated the following demands from PE traffic:")
pprint (flows,result_file)

wc_link_util = {} # list containing node_a - node_b link tuples and traffic levels for every failure
links=list(links)
for link in links:
	link_to_remove_1 = (link[0], link[1])
	link_to_remove_2 = (link[1], link[0])
	links.remove(link_to_remove_2)
	G.remove_edge(*link_to_remove_1)
	G.remove_edge(*link_to_remove_2)
	#wc_link_util.append(link_to_remove_1:x.Flows_to_Loads(flows,G))
	wc_link_util.update({link_to_remove_1:x.Flows_to_Loads(flows,G)})
	G.add_edge(*link_to_remove_1)
	G.add_edge(*link_to_remove_2)
wc_util = x.Worst_Case_Util(wc_link_util)	
print(result_file, "Worst case link utilisations:")
pprint (wc_util,result_file)

pprint (wc_link_util)





