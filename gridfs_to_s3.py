from pymongo import MongoClient
import re
import os
import shutil
filepath = '/home/ec2-user/tmpgridfs'
if not os.path.exists(filepath):
        try:
                os.makedirs(filepath)
        except:
                print("Can't create the directory.Exiting now")
                exit()
os.chdir(filepath)
uri="mongodb://localhost:27017"
connection=MongoClient(uri)
db = connection['example']
all_collection=[]
collections=db.collection_names()
for collection in collections:
        if re.search('.files', collection, flags=0):
                all_collection.append(collection)
for collection in all_collection:
    count=db[collection].count()
    if count !=0:
        if not os.path.exists(os.path.join(filepath,collection.split('.')[0])):
            try:
                os.makedirs(os.path.join(filepath,collection.split('.')[0]))
                print(os.path.join(filepath,collection.split('.')[0])+" directory got created")
            except:
                print("Can't create the directory for the collection.Exiting now")
                exit()
            os.chdir(os.path.join(filepath,collection.split('.')[0]))
            cursor=db[collection].find()
            for document in cursor:
                filename=document['filename']
                os.system("mongofiles --host localhost:27017 -d example get '"+filename+"' --prefix '"+collection.split('.')[0]+"'")
os.system("aws s3 sync /home/ec2-user/tmpgridfs s3://gridfs")
shutil.rmtree(filepath)
