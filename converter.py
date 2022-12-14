from stix2 import FileSystemSource,Filter

counter =0
row_counter=0


data={}
filesystemsource = FileSystemSource("stix_taxxi-main", allow_custom=True)

filter_objs = {"techniques": Filter("type", "=", "attack-pattern"),"malware": Filter("type", "=", "malware"),}

substring_true=lambda x,y: x in y

def ioc_check(ioc_string):
    """
    This function is used for validating the ioc details entered by the user.
    """
    ioc_data=filesystemsource.get(ioc_string)
    if(ioc_data==None):
        return 0
    else:
        return 1


def search(search_string):
    """
    This function is used for searching STIX-ID that user might be interested in using the keywords entered.
    """
    ioc_dictionary={}
    try:
        for key in filter_objs:
            data[key]=filesystemsource.query(filter_objs[key])
        pass
    except:
        print("Exception")

    for item in data:
        for iter in range(0,len(data[item])):
            ioc=data[item][iter]
            New_key="aliases"
            #print(ioc["name"])
            
            if(substring_true(search_string.upper(),ioc["name"].upper())):
                print(ioc["name"])
                ioc_dictionary[ioc["name"]]=ioc["id"]
            elif(substring_true(search_string.upper(),ioc["description"].upper())):
                ioc_dictionary[ioc["name"]]=ioc["id"]
            
    
    return ioc_dictionary
            
                
                
    
if __name__ == "__main__":
    ioc_check("test")


