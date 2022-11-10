from importlib.resources import path
from taxii2client.v20 import Collection, Server
from stix2 import FileSystemSource,utils
from datetime import date,datetime
import xlwt
import json
import time

def sdo_creater_date(rels,date_stix):
    sdos=[]
    sdos_rel=[]
    filesystemsource = FileSystemSource("stix_taxxi-main", allow_custom=True)
    for item in rels:
        key=list(item.keys())[0]
        sdo_r=item[key]
        sdo_v=filesystemsource.get(key)
        
        if(greater(sdo_v["modified"],date_stix)):
            sdos.append(sdo_v)
            sdos_rel.append(sdo_r)
        else:
            print("working")
    return(sdos,sdos_rel)

def sdo_creater(rels):
    sdos=[]
    sdos_rel=[]
    filesystemsource = FileSystemSource("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main", allow_custom=True)
    for item in rels:
        key=list(item.keys())[0]
        sdo_r=item[key]
        sdo_v=filesystemsource.get(key)
        sdos.append(sdo_v)
        sdos_rel.append(sdo_r)
    return(sdos,sdos_rel)


def getRelationships(id):
    path="C:/Users/sudes/Desktop/ThreatIntel/Relations/"

    relas=open(path+"relations.json","r")
    data = json.loads(relas.read())
    relations_list=data[id]

    return relations_list

def write_sheet():
    pass

greater =lambda x,y:x>y
not_null_check=lambda x:x!=""


def writer(ioc_data,date_input):
    # creating Workbook and storing data
    wBook = xlwt.Workbook()
    wSheet = wBook.add_sheet('Data')  # creating Workbook and storing data

    filesystemsource = FileSystemSource("C:/Users/sudes/Desktop/ThreatIntel/stix_taxxi-main", allow_custom=True)

    if(not_null_check(date_input)):
        date_string=utils.format_datetime(datetime.strptime(date_input,"%Y-%m-%d"))
        date_stix=utils.parse_into_datetime(date_string)
    else:
        print("date is null")
    start=time.time()
    
    print("doing a localised search")
    counter = 0

    try:
        print("Getting IOC data")
        ioc = filesystemsource.get(ioc_data)
        print("Getting Relationships")
        rels = getRelationships(ioc["id"])
        
        if(not_null_check(date_input)):
            sdo_tuple=sdo_creater_date(rels,date_stix)
        else:
            sdo_tuple=sdo_creater(rels)
        
        sdos=sdo_tuple[0]
        sdos_rel=sdo_tuple[1]
        
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
            wSheet.write(counter, 2, sdos_rel[i])
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
        
    finally:
        wBook.save("data.xls")
        print("File saved successfully in first loop")

        

    try:
        for j in range(0, min(10, len(sdos))):

            sdo_current = sdos[j]
            sdo_current_id=sdo_current['id']
            rels2 = getRelationships(sdo_current_id)
            
            
            # for every relation of extended sdo we are getting related sdo's
            if(not_null_check(date_input)):
                sdo_tuple2=sdo_creater_date(rels2,date_stix)
            else:
                sdo_tuple2=sdo_creater(rels2)
            sdos2=sdo_tuple2[0]
            sdos_rel2=sdo_tuple2[1]
            
           
                   
            for x in range(0, min(5, len(sdos2))):
                counter = counter+1
                wSheet.write(counter, 0, sdo_current["name"]+'/'+sdo_current["type"])
                wSheet.write(counter, 2, sdos_rel2[x])
                #print(sdos_rel2[x])
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


