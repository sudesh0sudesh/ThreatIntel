from pyvis.network import Network
from matplotlib import pyplot as plt

import pandas as pd
import networkx as nx
net = Network(notebook=False)
df = pd.read_excel("C:/Users/sudes/Desktop/ThreatIntel/data.xls")
#print(df)
G=nx.from_pandas_edgelist(df,source="source", target="Target",edge_attr="Relation")
edge_labels={}
edges=nx.edges(G)
nodes=nx.nodes(G)
#for i in range(0,len(df["source"])):
  #  edge
    

edge_labels= nx.get_edge_attributes(G,"Relation")
print(edge_labels)
pos = nx.spring_layout(G)
nx.draw_networkx_edge_labels(G,pos=pos, edge_labels=edge_labels)  


graph = Network()
graph.nodes= nodes
#net.from_nx(G)
#net.add_edges(edges)
print(graph.nodes)

#print(nx.edges(G)["Relation"])
#net.show("output.html")
#G[item[0]][item[1]]["Relation"]