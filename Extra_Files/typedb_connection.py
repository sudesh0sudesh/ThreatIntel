from typedb.client import *
client = TypeDB.core_client(address=TypeDB.DEFAULT_ADDRESS)
options= TypeDBOptions.core()
options.set_trace_inference= True
options.set_parallel = False
database = "cti"
Session_new= client.session(database, SessionType.DATA)
transaction_new= Session_new.transaction(TransactionType.WRITE)
query="match $malware isa malware, has name $abc; $attack-pattern isa attack-pattern, has name 'Exploitation of Remote Services' ;$use (used-by: $malware, used: $attack-pattern) isa use; limit 2;"
results=transaction_new.query().match(query)

#print(dir(results))
for result in results:
    print(result)
    print(result.get("use").is_thing())
       
        

    #print(dir(result))


