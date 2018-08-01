import networkx as nx
import sys
import re
from pprint import pprint

class GraphSolve(object):
	
	def __init__(self, all_pe_out = 0, pe_nodes = [],pe_demands = []): # constructor
		self.all_pe_out = all_pe_out # total traffic from all PE nodes
		self.pe_nodes = pe_nodes #list of all unique PE nodes
		self.pe_demands = pe_demands #list of PE to PE demands
		
	def Gravity(self,pe_traffic):
		'''demands are calculated from pe_traffic file'''
		traffic = {} # dictionary of arrays representing out and in traffic for every PE.
		demands_file = open(pe_traffic,"r").readlines()
		firstLine = demands_file.pop(0)
		for line in demands_file:
			pe,traffic_in,traffic_out = line.split(",")
			self.pe_nodes.append(pe)
			traffic[pe] = [traffic_out,traffic_in]
			self.all_pe_out = self.all_pe_out + int(traffic_out)
		while len(self.pe_nodes) > 1: # produces PE to PE full demand mesh
			for i in range (0,len(self.pe_nodes)-1):
				self.pe_demands.append ((self.pe_nodes[0], self.pe_nodes[i+1]))
				self.pe_demands.append ((self.pe_nodes[i+1], self.pe_nodes[0]))
			del self.pe_nodes[0]
		#formula to calculate demand values: pe2_in*pe1_out/(all_pe_out-pe2_out)
		demands_matrix = {}
		for pe in self.pe_demands:
			demand_value = int(traffic[pe[1]][1])*int(traffic[pe[0]][0])/(self.all_pe_out-int(traffic[pe[1]][0]))
			demands_matrix.update({(pe[0],pe[1]):demand_value})
		return demands_matrix

	def SP_Edge(self,shortest_path,traffic):
		'''for the given demand's shortest path add traffic for each edge'''
		new = {}
		for a in range(0,len(shortest_path)-1,1):
			new.update({(shortest_path[a], shortest_path[a+1]):traffic})
		return new
		
	def Flows_to_Loads(self,flows,G):
		'''
		Maps the flows to the link utilisations
		'''
		dict_final = {}
		shortest_path = []
		for demand_key, traffic in flows.items():
			shortest_path = list(nx.shortest_path(G, demand_key[0], demand_key[1], weight="weight"))
			edges = self.SP_Edge(shortest_path,traffic)
			for key, volume in edges.items():
				if key in dict_final:
					dict_final[key] = int(dict_final[key]) + int(edges[key])
				else:
					dict_final.update(edges)
		return dict_final
		
	def Worst_Case_Util(self,wc_link_util):
		dict_final = {}
		wc_failures = {}
		for failure, link_utilisations in wc_link_util.items():
			for link, volume in link_utilisations.items():
				if link in dict_final and int(dict_final[link]) < int(volume):
					dict_final[link] = volume
					total = str(link) + str(-volume)
					wc_failures[total] = failure
				elif link not in dict_final:
					dict_final[link] = volume
					total = str(link) + str(-volume)
					wc_failures[total] = failure
		return wc_failures
			
			
	
	
	

