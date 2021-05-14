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
all_collection=["uploadAssessorPhoto.files"]
uri="mongodb://PRD1:27017,PRD2:27017,PRD3:27017/db?replicaSet=prod"
connection=MongoClient(uri)
connection.the_database.authenticate('db', 'password1086#',source='db')
db = connection['db']
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
					print(str(document))
					print(filenamenew)
					db.assessors.update({'photo':str(document['_id'])},{'$set':{'photo':filenamenew}})
				except:
					print("Can not update trainers collection"+str(document['_id']))
					break
				try:
					os.system("mongofiles -d db get '"+filenameold+"' --prefix '"+collection.split('.')[0]+"' --username admin --password shal1086# --authenticationDatabase db")
				except:
					print("Can not download file"+filenameold)
					break
				try:
					os.rename(filenameold,filenamenew)
				except:
					print("Error renaming file"+str(document['_id']))
					break
