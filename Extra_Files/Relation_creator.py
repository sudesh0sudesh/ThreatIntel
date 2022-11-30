import json
from stix2 import  FileSystemSource, TAXIICollectionSource, Filter, Bundle,FileSystemSink,FileSystemStore


filesystemsource = FileSystemSource("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main", allow_custom=True)

filter_objs = {"malware": Filter("type", "=", "malware")}
data ={}
relations={}
try:
    for key in filter_objs:
        data[key]=filesystemsource.query(filter_objs[key])
    
except:
    print("Exception")

for item in data:
    for iter in range(0,len(data[item])):
        ioc=data[item][iter]
        rels = filesystemsource.related_to(ioc["id"], target_only=False)
        relationships = filesystemsource.relationships(ioc["id"],target_only=False)
        relation_list=[]
        for y in range(0,len(rels)):
            relation_pair={rels[y]["id"]:relationships[y]["relationship_type"]}
            relation_list.append(relation_pair)
            print(iter,y)
        relations[ioc["id"]]=relation_list
        

#print(relations["attack-pattern--43e7dc91-05b2-474c-b9ac-2ed4fe101f4d"])

file_open = open("relations.json","w")

json.dump(relations,file_open)

file_open.close()
        
    