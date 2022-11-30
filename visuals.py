from pyvis.network import Network
from flask import url_for
from stix2 import parse
import pandas as pd
import networkx as nx
import random




# reading node using pandas


#combining all the data and zipping them to form single file.
#easy for iteration

image_path="static/images/"
templates="templates/"

def new_net_props():
  net = Network(notebook=False,height='100%', width='50%', bgcolor='#222222', font_color='white')
  net.set_template("templates/template.html")
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
  return net
         

def dataRead():
   
    df = pd.read_excel("data.xls")
    source=df["source"]
    target= df["Target"]
    relation= df["Relation"]
    description= df["Description"]
    references= df["References"]
    tar_description = df["Target_Description"]
    tar_details=df["Target_References"]
    edge_info=0
    edge_info = zip(source, target,relation,description,references,tar_description, tar_details)
    return edge_info

def visual():
    
    edge_info=dataRead()
    tdes_html=0
    net= new_net_props()
    new_random= ''.join((random.choice('abcdefghizklmnopqrstuvwxyz') for i in range(18)))
    for item1 in edge_info:
      src=item1[0]
      dst=item1[1]
      rel=item1[2]
      des=item1[3]
      refs=item1[4]
      tdes=item1[6]
      #print(type(item[6]))
      tdes_stix=parse(tdes,allow_custom=True)
      #tdes_neat=tdes_stix.serialize(pretty=True)
      tdes_html="<ul class='list-group'>"
      for item in tdes_stix:
        head=item.upper()
        if("X_MITRE" not in head and "EXTERNAL_REFERENCES" not in head and "KILL_CHAIN_PHASES" not in head and "OBJECT_MARKING_REFS" not in head and  "CREATED_BY_REF" not in head and "REVOKED" not in head and "DESCRIPTION" not in head):
          tdes_html=tdes_html+"<li><b>"+head+": </b>"+str(tdes_stix[item]) + "</li>"
        elif("DESCRIPTION"== head):
          tdes_html=tdes_html+"<li><div class='accordian accordion-flush' id='accordian-des'><div class='accordian-item border-0'><b>"+head
          tdes_html=tdes_html+"</b><button class='btn-close btn' type='button' data-bs-toggle='collapse' data-bs-target='#accordbodyfordes' aria-expanded='false' aria-controls='#accordbodyfordes'></button>"
    
          tdes_html=tdes_html+"<div class=' border-0 accordion-collapse collapse accordian-body show' id='accordbodyfordes' data-parent='#accordian-des'>"+str(tdes_stix[item])+"</div></div></div></li>"
        elif("KILL_CHAIN_PHASES"== head):
          tdes_html=tdes_html+"<li><b>"+head+": </b>"+"<ol>"

          for entity in tdes_stix[item]:
            tdes_html=tdes_html+"<li>"+entity.get("phase_name")+"</li>"
          tdes_html=tdes_html+"</ol></li>"

          print(tdes_stix[item][0]["phase_name"]) 
        elif("EXTERNAL_REFERENCES"== head):
          tdes_html=tdes_html+"<li class='list-group-item list-group-item-action'><div class='accordian' id='accordian'><div class='accordian-item list-group' data-bs-toggle='collapse' data-bs-target='#accordbody' aria-expanded='true' aria-controls='#accordbody'><b><button class='accordion-button accordion-header' type='button'>"+head+": </b>"+"</button><div class='collapse' id='accordbody'data-parent='#accordian'><ol class='accordion-body'>"
          for reference in tdes_stix["external_references"]:
            if("url" in reference):
              tdes_html=tdes_html+"<li class='list-group-item'></b>"+"<a target='_blank' href="+reference["url"]+">"+reference["source_name"]+"</a>"+"</li>"
          tdes_html=tdes_html+"</ol></div></div></div></li>"
              
      tdes_html=tdes_html+"</ul>" 
              
          
        
          
          
      
               
      net.add_node(src, src, title=des,shape="star")
      if(tdes_stix["type"]=="attack-pattern"):
          net.add_node(dst, dst,title=tdes_html, shape="image", image="https://oasis-open.github.io/cti-documentation/img/icons/attack_pattern.png")
      elif(tdes_stix["type"]=="malware"):
          net.add_node(dst, dst,title=tdes_html, shape="image", image="https://oasis-open.github.io/cti-documentation/img/icons/malware.png")
      elif(tdes_stix["type"]=="intrusion-set"):
          net.add_node(dst, dst,title=tdes_html, shape="image", image="https://oasis-open.github.io/cti-documentation/img/icons/intrusion_set.png")
      elif(tdes_stix["type"]=="tool"):
          net.add_node(dst, dst,title=tdes_html, shape="image", image="https://oasis-open.github.io/cti-documentation/img/icons/tool.png")
      elif(tdes_stix["type"]=="course-of-action"):
          net.add_node(dst, dst,title=tdes_html, shape="image", image="https://oasis-open.github.io/cti-documentation/img/icons/course_of_action.png")
      else:
          net.add_node(dst, dst,title=tdes_html, shape="dot")
      net.add_edge(src,dst,label=rel, color="#0D77EE",)
    
    #print(net.options["edges"])
    #net.set_template("template.html")
    #net.show_buttons(filter_=['interaction'])
    #net.write_html("template.html")
    #net.template="template.html"
    #net.show("sample1.html")
    #net.set_template("templates/template.html")
    
    net.write_html(name=templates+new_random+".html")
    return(new_random+".html")

if __name__ == "__main__":
  visual()
#running the visual

      
    
    
