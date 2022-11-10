
from pyvis.network import Network
from matplotlib import pyplot as plt
from stix2 import parse
import pandas as pd
import networkx as nx
net = Network(notebook=False,height='100%', width='50%', bgcolor='#222222', font_color='white')
df = pd.read_excel("C:/Users/sudes/Desktop/ThreatIntel/data.xls")
source=df["source"]
target= df["Target"]
relation= df["Relation"]
description= df["Description"]
references= df["References"]
tar_description = df["Target_Description"]
tar_details=df["Target_References"]
image_path="images/"

edge_info = zip(source, target,relation,description,references,tar_description, tar_details)

for item in edge_info:
    src=item[0]
    dst=item[1]
    rel=item[2]
    des=item[3]
    refs=item[4]
    tdes=item[6]
    #print(type(item[6]))
    tdes_stix=parse(tdes,allow_custom=True)
    tdes_neat=tdes_stix.serialize(pretty=True)
    tdes_html="<ul>"
    for item in tdes_stix:

      tdes_html=tdes_html+"<li><b>"+item.upper()+":</b>"+str(tdes_stix[item]) + "</li>"

      
    tdes_html+"</ul>"
    net.add_node(src, src, title=des,shape="star")
    if(tdes_stix["type"]=="attack-pattern"):
        net.add_node(dst, dst,title=tdes_html, shape="image", image=image_path+"attack_pattern.png")
    elif(tdes_stix["type"]=="malware"):
        net.add_node(dst, dst,title=tdes_html, shape="image", image=image_path+"malware.png")
    elif(tdes_stix["type"]=="intrusion-set"):
        net.add_node(dst, dst,title=tdes_html, shape="image", image=image_path+"intrusion_set.png")
    elif(tdes_stix["type"]=="tool"):
        net.add_node(dst, dst,title=tdes_html, shape="image", image=image_path+"tool.png")
    else:
        net.add_node(dst, dst,title=tdes_html, shape="dot")

    net.add_edge(src,dst,label=rel, color="#0D77EE",)
net.set_options('''const options = {
  "interaction": {
    "tooltipDelay": 86500000,
    "zoomSpeed": 0.01
  },

  "edges": {
    "arrows": {
      "to": {
        "enabled": true
      },
    "color":"#0BF607",
    "hightlight":"#0D77EE"
    },
    "color":{
    "color":"#0D77EE",
    "hightlight":"green",
    "inherit":false
    }
	},
"nodes": {
    "shadow": {
      "enabled": true
    },
    "shape": "triangle",
    "shapeProperties": {
      "borderDashes": true,
      "borderRadius": 19
    },
    "size": 20
  }
}''')
print(net.options["edges"])
#net.set_template("template.html")
#net.show_buttons(filter_=['interaction'])
#net.write_html("template.html")
#net.template="template.html"
net.show("sample1.html")


