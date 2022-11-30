import json

path="C:/Users/sudes/Desktop/ThreatIntel/Relations/"
relas=open(path+"relations.json","r")
data = json.loads(relas.read())
relations_list=data["malware--94379dec-5c87-49db-b36e-66abc0b81344"]

for item in relations_list:
    i=0
    sdos=[]
    sdos_rel=[]
    key=list(item.keys())[0]
    sdo_r=item[key] 
    print(sdo_r) 
      
    sdos_rel.insert(i,sdo_r)
    i=i+1

print(sdos_rel)