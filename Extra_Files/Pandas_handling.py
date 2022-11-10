from pyvis.network import Network
from matplotlib import pyplot as plt

import pandas as pd
import networkx as nx
net = Network(notebook=False)
df = pd.read_excel("C:/Users/sudes/Desktop/ThreatIntel/data.xls")
print (df["source"])