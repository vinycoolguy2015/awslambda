import gridfs
from pymongo import MongoClient


if __name__ == '__main__':

# read in the image.   
    filename = "red_fort.jpg"
    datafile = open(filename,"r");
    thedata = datafile.read()

# connect to database

    connection = connection = MongoClient('mongodb://localhost:27017')
    database = connection['example']

# create a new gridfs object.
    fs = gridfs.GridFS(database,"test")

# store the data in the database. Returns the id of the file in gridFS
    stored = fs.put(thedata, filename="red_fort")
