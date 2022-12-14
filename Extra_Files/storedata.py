from taxii2client.v20 import Collection, Server
from stix2 import CompositeDataSource, FileSystemSource, TAXIICollectionSource, Filter, Bundle,FileSystemSink,FileSystemStore
import requests
import stix2viz
import xlwt

wBook = xlwt.Workbook()
wSheet = wBook.add_sheet('Data')
counter =0
row_counter=0

#TAXII
#create TAXIICollectionSource from MITRE
server = Server("https://cti-taxii.mitre.org/taxii/") #Choose server
api_root = server.api_roots[0]

#all of collections from MITRE taxii server
collection0 = Collection(api_root.collections[0].url) 
taxiicollectionsource0 = TAXIICollectionSource(collection0)
print(api_root.collections[0].url)



#create FileSystemSource
filesystemsource = FileSystemSource("stix_taxxi-main", allow_custom=True)
fssink =  FileSystemSink("stix_taxxi-main/", allow_custom=True)
fsstore=FileSystemStore("stix_taxxi-main/", allow_custom=True)

#adding taxii collections of local and online sources to create a CompositeDataSource
compositedatasource = CompositeDataSource() #This is used for use local taxii intelligence and public taxii server
compositedatasource.add_data_sources([filesystemsource,taxiicollectionsource0])


#MAIN

##performing search through composite data source
search="malware**"
print("Creating localized repository")


ioc = compositedatasource.get(search) #Get the SDO of the 'ioc' introduced

rels = compositedatasource.relationships(ioc["id"],target_only=False) #Get all the relationships related to the 'ioc'

sdos = compositedatasource.related_to(ioc["id"], target_only=False) #Get all the SDOs related to the 'ioc'


#writing the data to filesystem.

for x in range(0,len(rels)):
    if(fsstore.get(rels[x]["id"])==None):
            fssink.add(rels[x])

for j in range(0,len(sdos)):     
    sdos2 = compositedatasource.related_to(sdos[j]['id'], target_only=False)
    rels2 = compositedatasource.relationships(sdos[j]['id'],target_only=False)
    #print(sdos2)
    print(sdos2[0])
    for x in range(0,len(sdos2)):
        if(fsstore.get(sdos2[x]["id"])==None):
            fssink.add(sdos2[x])
        if(fsstore.get(rels2[x]["id"])==None):
            fssink.add(rels2[x])
    
        
     
        


