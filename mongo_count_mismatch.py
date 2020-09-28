#This script can be used to check any data mismatch between 2 mongo servers. 
#Initially written to verify data integrity after database migration from ATLAS to self-hosted mongo server.

from pymongo import MongoClient
databases=['a','b']
new_server = MongoClient('mongo1.analytics.in',username='',password='',authSource='admin',authMechanism='SCRAM-SHA-1',ssl=True)
atlas_server = MongoClient('cluster-shard-00-00.mongodb.net',username='',password='',authSource='admin',authMechanism='SCRAM-SHA-1',ssl=True)

for database in databases:
    atlas_db=atlas_server[database]
    new_db=new_server["t_"+database]
    for collection in atlas_db.collection_names():
        atlas_count=atlas_db[collection].count()
        new_server_count=new_db[collection].count()
        if atlas_count != new_server_count:
            print "Count mismatch for " +database+"."+collection+" atlas_count:"+ str(atlas_count)+" new_server_count:"+str(new_server_count)
