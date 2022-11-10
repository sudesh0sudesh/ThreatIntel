from taxii2client.v21 import Server, Collection
from stix2 import parse
server = Server('http://127.0.0.1:5000/trustgroup1', user='admin', password='Password0')
api_root = server.api_roots[2]
collection = api_root.collections[2]
diction = Collection.get_objects("localhost:5000/trustgroup1/collections/90c00720-636b-4485-b342-8751d232bf09/")
diction=collection.get_objects()

for i in diction:
    if ((diction["more"]==False) & (diction["objects"]!="")):
        for j in diction["objects"]:
           for y in j:
            if(j[y]=="attack-pattern"):
                print(parse(j).serialize(pretty=True))
        print("____________Object_________")
           

