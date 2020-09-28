import time
from pymongo import MongoClient
from datetime import datetime,timedelta
import ssl

new_server = MongoClient(['mongo1.analytics.in','mongo2.analytics.in','mongo3.analytics.in'],replicaset='mongo',username='',password='',authSource='admin',authMechanism='SCRAM-SHA-1',ssl=True)

atlas_server = MongoClient(['cluster-shard-00-00.mongodb.net','cluster-shard-00-01.mongodb.net','cluster-shard-00-02.mongodb.net'],replicaset='cluster-shard-0',username='',password='',authSource='admin',authMechanism='SCRAM-SHA-1',ssl=True)

server = MongoClient(['mongo1.care.in:27017','mongo2.care.in:27017','mongo4.care.in:27017'],replicaset='repl',username='',password='',authSource='admin',authMechanism='SCRAM-SHA-1',ssl=True,ssl_cert_reqs = ssl.CERT_NONE)

isodate = datetime.today() - timedelta(days=30)

for database in server.database_names():
    if database not in ['admin','config','local']:
        db=server[database]
        collection=db['apilogs']
        collection.remove({'createdDate':{'$lte':isodate}})
        print "Data deleted from " +database +".apilogs"



for database in new_server.database_names():
    if database not in ['admin','config','local']:
        db=new_server[database]
        collection=db['apilogs']
        collection.remove({'createdDate':{'$lte':isodate}})
        print "Data deleted from " +database +".apilogs"

for database in atlas_server.database_names():
    if database not in ['admin','config','local']:
        db=atlas_server[database]
        collection=db['apilogs']
        collection.remove({'createdDate':{'$lte':isodate}})
        print "Data deleted from " +database +".apilogs"
