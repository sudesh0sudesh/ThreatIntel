from taxii2client.v20 import Collection, Server
from stix2 import CompositeDataSource, FileSystemSource, TAXIICollectionSource, Filter, Bundle,FileSystemSink,FileSystemStore


counter =0
row_counter=0

#TAXII
#create TAXIICollectionSource from MITRE
server = Server("https://cti-taxii.mitre.org/taxii/") #Choose server
api_root = server.api_roots[0]
collection_url=[]
for item in api_root.collections:
    collection_url.append(item.url)

#all of collections from MITRE taxii server
collection0 = Collection(api_root.collections[0].url) 
taxiicollectionsource0 = TAXIICollectionSource(collection0)
print(api_root.collections[0].url)



#create FileSystemSource
filesystemsource = FileSystemSource("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main", allow_custom=True)
fssink =  FileSystemSink("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main/", allow_custom=True)
fsstore=FileSystemStore("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main/", allow_custom=True)

data={}


#MAIN

filter_objs = {"techniques": Filter("type", "=", "attack-pattern"),
          "mitigations": Filter("type", "=", "course-of-action"),
          "groups": Filter("type", "=", "intrusion-set"),
          "malware": Filter("type", "=", "malware"),
          "tools": Filter("type", "=", "tool"),
          "relationships": Filter("type", "=", "relationship")
}

try:
    #for key in filter_objs:
     #   data[key]=taxiicollectionsource0.query(filter_objs[key])
    pass
except:
    print("Exception")

#for item in data:
    
    #for i in range(0,len(data[item])):
       # print(i)
        #if(fsstore.get(data[item][0]["id"])==None):
        #    fssink.add(data[item][0])
        #else:
        #    pass
        

    