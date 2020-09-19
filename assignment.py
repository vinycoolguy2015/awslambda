import json
from datetime import datetime
import argparse


def load_data(filename):
    with open(filename, 'r') as myfile:
        data=myfile.read()

    return json.loads(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',required=True,help="specify json filepath")
    parser.add_argument('--retention_days',required=True,help="specify retention duration")
    args = parser.parse_args()
    
    #Read data
    data=load_data(args.filepath)
    
    #Parse data
    image_count=0
    for record in data:
        date_created=record['creationTimestamp'][0:10]
        if (datetime.today() - datetime.strptime(date_created,'%Y-%m-%d')).days > int(args.retention_days):
            image_count+=1
            
    #Output
    print("Count of Images older than {} is {}".format(args.retention_days,image_count))
            
    
                    
if __name__ == "__main__":
	main()
