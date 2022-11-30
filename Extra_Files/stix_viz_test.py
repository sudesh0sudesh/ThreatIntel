from taxii2client.v20 import Collection, Server
from stix2 import CompositeDataSource, FileSystemSource, TAXIICollectionSource, Filter, Bundle,FileSystemSink,FileSystemStore
import xlwt
import json

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
taxiicollectionsource0 = TAXIICollectionSource(collection0,allow_custom=True)
print(api_root.collections[0].url)



#create FileSystemSource
filesystemsource = FileSystemSource("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main", allow_custom=True)
fssink =  FileSystemSink("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main/", allow_custom=True)
fsstore=FileSystemStore("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main/", allow_custom=True)

#add taxii collections (server and local) to the CompositeDataSource
compositedatasource = CompositeDataSource() #This is used for use local taxii intelligence and public taxii server
compositedatasource.add_data_sources([filesystemsource,taxiicollectionsource0])


#MAIN

#search = input("Enter the SDO you are searching: (example: malware--94379dec-5c87-49db-b36e-66abc0b81344)")
search="malware--94379dec-5c87-49db-b36e-66abc0b81344"
print("Wait a moment please. This search may take a few minutes")


ioc = compositedatasource.get(search) #Get the SDO of the 'ioc' introduced

rels = compositedatasource.relationships(ioc["id"],target_only=False) #Get all the relationships related to the 'ioc'

sdos = compositedatasource.related_to(ioc["id"], target_only=False) #Get all the SDOs related to the 'ioc'


wSheet.write(0, 0, "source")
wSheet.write(0, 1, "Target")
wSheet.write(0, 2, "Relation")

wSheet.write(0, 3, "Description")
wSheet.write(0, 4, "References")

wSheet.write(0, 5, "Target_Description")
wSheet.write(0, 6, "Target_References")

#print(dir(ioc))
#print(type(ioc))
json_new=json.loads(ioc.serialize())
#ioc=json_new



counter=0 #counter to track rows in sheet that we will be writing into.

try:
    for i in range(0,min(10,len(sdos))):
        counter=counter+1
        # sdos references, Json conversion
        
        sdo_temp = json.loads(sdos[i].serialize())
        #sdo_temp=json_new
        
        wSheet.write(counter, 0, ioc['name']+'/'+ioc['type'])
        wSheet.write(counter, 2, rels[i]['relationship_type'])
        wSheet.write(counter, 1, sdo_temp['name']+'/'+sdo_temp['type'])
        #description
        wSheet.write(counter, 3, str(ioc['description']))
        wSheet.write(counter, 4, str(ioc['external_references']))
        #target details
        wSheet.write(counter, 5, str(sdo_temp['description']))
        wSheet.write(counter, 6, str(sdos[i]))


        
        

        print(counter) 
except Exception as e:
    print("Issue with first loop")
    print(e)
    
finally:
    wBook.save("data.xls")
    print("File saved successfully in first loop")




try:
    for j in range(0,min(5,len(sdos))):     
        sdos2 = compositedatasource.related_to(sdos[j]['id'], target_only=False)
        rels2 = compositedatasource.relationships(sdos[j]['id'],target_only=False)
        
        #print(sdos2)
        #print(sdos2[0])
        for x in range(0,min(5,len(sdos2))):
            counter =  counter+1
            wSheet.write(counter, 0, sdos[j]["name"]+'/'+sdos[j]["type"])
            wSheet.write(counter, 2, rels2[x]['relationship_type'])
            wSheet.write(counter, 1, sdos2[x]['name']+'/'+sdos2[x]["type"])
            #description
            wSheet.write(counter, 3, sdos[j]['description'])
            wSheet.write(counter, 4, str(sdos[j]['external_references']))
            #target description
            wSheet.write(counter, 5, str(sdos2[x]['description']))
            wSheet.write(counter, 6, str(sdos2[x]))
except Exception as e:
    print(e)
    print("Issue with second loop")
        
finally:
    wBook.save("data.xls")    

