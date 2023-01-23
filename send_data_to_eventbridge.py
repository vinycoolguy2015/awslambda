#https://aws-dojo.com/excercises/excercise14/

import boto3

client = boto3.client('events')

response = client.put_events(Entries=[ { 'Source': 'source1', 'DetailType': 'testdetails', 'Detail': '{ "name": "Vinayak" }' },])

print(response)

#Event Rule Pattern
#{
#  "detail": {
#    "name": [{
#      "prefix": "Vinayak"
#    }]
#  }
#}
