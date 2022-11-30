from taxii2client.v20 import Collection, Server
from stix2 import FileSystemSource, TAXIICollectionSource, Filter, Bundle, FileSystemSink, FileSystemStore
import xlwt
import json
import time


def writer(ioc_data):

    # creating Workbook and storing data
    wBook = xlwt.Workbook()
    wSheet = wBook.add_sheet('Data')  # creating Workbook and storing data

    filesystemsource = FileSystemSource(
        "C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main", allow_custom=True)


    start=time.time()
    
    print("doing a localised search")
    counter = 0
    try:
        print("Getting IOC data")
        ioc = filesystemsource.get(ioc_data)
        print("Getting Relationships")
        rels = filesystemsource.relationships(ioc["id"], target_only=False)
        #print(rels[0])
        sdos=[]
        for item in rels:
            if(ioc_data==item["source_ref"]):
                sdo_v= filesystemsource.get(item["target_ref"])
                if(sdo_v !=None):
                    sdos.append(sdo_v)
                else:
                    rels.remove(item)
                
            else:
                 sdo_v= filesystemsource.get(item["source_ref"])
                 if(sdo_v !=None):
                    sdos.append(sdo_v)
                 else:
                    rels.remove(item)
                
        #print(sdos[0])
        
        
    except Exception as e:
        print("Issue with initial Fetch and find the issue below:")
        print(e)

# writing Heads or coloumn names.

    wSheet.write(0, 0, "source")
    wSheet.write(0, 1, "Target")
    wSheet.write(0, 2, "Relation")
    wSheet.write(0, 3, "Description")
    wSheet.write(0, 4, "References")
    wSheet.write(0, 5, "Target_Description")
    wSheet.write(0, 6, "Target_References")

    try:
        for i in range(0, min(10, len(sdos))):
            # first major loop writing the data
            counter = counter+1
            # sdos references, Json conversion

            sdo_temp = json.loads(sdos[i].serialize())
            # sdo_temp=json_new

            wSheet.write(counter, 0, ioc['name']+'/'+ioc['type'])
            wSheet.write(counter, 2, rels[i]['relationship_type'])
            wSheet.write(counter, 1, sdo_temp['name']+'/'+sdo_temp['type'])
            # description
            wSheet.write(counter, 3, str(ioc['description']))
            wSheet.write(counter, 4, str(ioc['external_references']))
            # target details
            wSheet.write(counter, 5, str(sdo_temp['description']))
            wSheet.write(counter, 6, str(sdos[i]))

    except Exception as e:
        print("Issue with the first major loop")
        print(e)
        print(i)
    finally:
        wBook.save("data.xls")
        print("File saved successfully in first loop")

        

    try:
        for j in range(0, min(10, len(sdos))):

            end = time.time()
            print(str(end-start)+" time before relations pulling")
            sdo_current = sdos[j]
            sdo_current_id=sdo_current['id']
            rels2 = filesystemsource.relationships(sdo_current_id,relationship_type=None, target_only=False, source_only=False,)
            sdos2=[]
            
            # for every relation of extended sdo we are getting related sdo's
            end = time.time()
            print(str(end-start)+"time after pulling relations ")

            for item in rels2:
                if(sdo_current_id==item["source_ref"]):
                    sdo_v2= filesystemsource.get(item["target_ref"])
                    if(sdo_v2 !=None):
                         sdos2.append(sdo_v2)
                    else:
                        rels2.remove(item)
                
                   
                else:
                    sdo_v2= filesystemsource.get(item["source_ref"])

                    if(sdo_v2 !=None):
                         sdos2.append(sdo_v2)
                    else:
                        rels2.remove(item)

                
            

            
            for x in range(0, min(5, len(sdos2))):
                counter = counter+1
                wSheet.write(counter, 0, sdo_current["name"]+'/'+sdo_current["type"])
                wSheet.write(counter, 2, rels2[x]['relationship_type'])
                wSheet.write(counter, 1, sdos2[x]['name']+'/'+sdos2[x]["type"])
                # description
                wSheet.write(counter, 3, sdo_current['description'])
                wSheet.write(counter, 4, str(sdo_current['external_references']))
                # target description
                wSheet.write(counter, 5, str(sdos2[x]['description']))
                wSheet.write(counter, 6, str(sdos2[x]))
        
    except Exception as e:
        print(e)
        print("Issue with second loop")
        return 0

    finally:
        wBook.save("data.xls")
        print("File saved successfully")
        return 1


writer("malware--94379dec-5c87-49db-b36e-66abc0b81344")
