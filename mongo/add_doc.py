import re
import os
from pymongo import MongoClient
import shutil

filepath = "/home/centos/gridfs"
if not os.path.exists(filepath):
        try:
                os.makedirs(filepath)
        except:
                print("Can't create the directory.Exiting now")
                exit()
os.chdir(filepath)
client = MongoClient()
db = client.mydb
all_collection=["documentsAddedByFCForTC.files"]
for collection in all_collection:
	path=filepath+'/'+collection.split('.')[0]
	count=db[collection].count()
	if count !=0:
		if not os.path.exists(path):
			try:
				os.makedirs(path)
			except:
				print("Can't create the directory.Exiting now")
				exit()
			os.chdir(path)
			cursor=db[collection].find()
			for document in cursor:
				filenameold=document['filename']
				filenamenew=str(document['_id'])+"_"+filenameold
				try:
					db.trainingcentres.update({'documentSubmittedByFC.id':str(document['_id'])},{'$set':{'documentSubmittedByFC.id':filenamenew}})
				except:
					print("Can not update students collection"+str(document['_id']))
				try:
					os.system("mongofiles -d mydb get '"+filenameold+"' --prefix '"+collection.split('.')[0]+"'")
				except:
					print("Can not download file"+filenameold)
				try:
					os.rename(filenameold,filenamenew)
				except:
					print("Error renaming file"+str(document['_id']))

