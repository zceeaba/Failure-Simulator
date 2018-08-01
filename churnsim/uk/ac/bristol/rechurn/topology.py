import networkx as nx
import csv
import os.path
import collections
import pylab
import matplotlib.pyplot as plt

class Topology(nx.Graph):

    def load_from_csvs(self, nodes_csv, edges_csv):
        """
           This function generates a Graph object based on a list of nodes and a list of adjacency pairs
           inputs:
               nodes_csv: Absolute path to a CSV file with the following structure
                          Name,Historical Significance,Gender,Birthdate,Deathdate,ID
                          Joseph Wyeth,religious writer,male,1663,1731,10013191
                          Alexander Skene of Newtyle,local politician and author,male,1621,1694,10011149
               edges_csv: Absolute path to a CSV file with the following structure
                          Source,Target
                          George Keith,Robert Barclay
                          George Keith,Benjamin Furly
           return successful: boolean indicating whether the load of both files was successful or not
        """
        if (not(os.path.exists(nodes_csv) and os.path.isfile(nodes_csv)
                and os.path.exists(edges_csv) and os.path.isfile(edges_csv))):
            return False

        # Name,Historical Significance,Gender,Birthdate,Deathdate,ID
        node_headers = []

        with open(nodes_csv, 'r') as nodecsv:
            nodereader = csv.reader(nodecsv)
            node_headers = next(nodereader)
            nodes = [n for n in nodereader][1:]

        node_names = [n[0] for n in nodes]
        with open(edges_csv, 'r') as edgecsv:
            edgereader = csv.reader(edgecsv)
            edges = [tuple(e) for e in edgereader][1:]

        self.add_nodes_from(node_names)
        self.add_edges_from(edges)

        # load attributes of the nodes
        attributes = collections.defaultdict(dict)

        for i in range(1,len(node_headers)):
            for node in nodes:
                attributes[node_headers[i]][node[0]] = node[i]

        for i in range(1, len(node_headers)):
            nx.set_node_attributes(self, name=node_headers[i], values=dict(attributes[node_headers[i]]))


        return True

    def load_from_json(self):
        import json
        nodes=[]
        edges=[]

        with open('../routerJSON.txt', 'r') as nodejson:
            message = nodejson.read()
            d = json.loads(message)
            nodes = d["nodes"]


        node_names = [n["name"] for n in nodes]

        with open('../routerJSON.txt', 'r') as edgejson:
            message = edgejson.read()
            d = json.loads(message)
            edges = d["links"]

        edgessd=[]
        result=list()
        for x in edges:
            tupleinput=(x["source"],x["destination"])
            edgessd.append(tupleinput)

        self.add_nodes_from(node_names)
        self.add_edges_from(edgessd)


        for n in nodes:
            for x in n.keys():
                if x=="name":
                    continue
                else:
                    self.node[n["name"]][x]=n[x]

        for x in edges:
            source=x["source"]
            destination=x["destination"]
            self[source][destination]['latency']=x['latency']

        #print(nx.get_edge_attributes(self,'latency'))

        #nx.draw(self)
        #plt.show()

        return True

    def load_from_google(self):

        with open('../google-cluster-data-1.csv', 'r') as nodecsv:
            nodereader = csv.DictReader(nodecsv,delimiter=' ')
            node_headers = next(nodereader)
            nodes = [n for n in nodereader][1:]

        #print(node_headers)
        node_names = [n["ParentID"] for n in nodes]
        #primarynode=node_names
        secondarynode=[n["TaskID"] for n in nodes]
        primarynode=node_names

        #print(node_names)



        edges = list(zip(primarynode,secondarynode))

        keys=[]
        node_names=list(set(node_names))

        self.add_nodes_from(node_names)


        self.add_edges_from(edges)

        print(len(node_names))
        print(len(edges))
        #print(self.edges)

        for x in nodes:
            self[x["ParentID"]][x["TaskID"]]["JobType"]=x["JobType"]
            self[x["ParentID"]][x["TaskID"]]["NrmlTaskCores"]=x["NrmlTaskCores"]
            self[x["ParentID"]][x["TaskID"]]["NrmlTaskMem"]=x["NrmlTaskMem"]
            self[x["ParentID"]][x["TaskID"]]["Time"]=x["Time"]



        #print(nx.get_edge_attributes(self,'Time'))

        return True


    def get_FTA_tab_dataset(self):
        import csv

        with open('..\clouddatalanl\event_trace.tab','r') as f:
            node_headers=next(f)
            reader=csv.reader(f,delimiter='\t')
            nodes = [n for n in reader]
            #print(nodes)

        for i in nodes:
            for x in range(len(i)):
                i[x]=(i[x]).strip()

        for i in nodes:
            print(i)

        node_headers = node_headers.replace("#", "")
        node_headers=[i for i in node_headers.split()]
        print(node_headers)

        node_names=[n[2] for n in nodes]
        unique_node_names=list(set(node_names))

        self.add_nodes_from(unique_node_names)

        eventnumbers=[n[0] for n in nodes]
        edges=list(zip(node_names,eventnumbers))


        self.add_edges_from(edges)

        for x in nodes:
            self[x[2]][x[0]]["start_time"]=x[6]
            self[x[2]][x[0]]["end_time"]=x[7]
            self[x[2]][x[0]]["end_reason"]=x[8]

        for x in nodes:
            edgedata=self[x[2]][x[0]]

        return True

    def bittorrenttopology(self):
        