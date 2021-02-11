import json
import sys
import random
import urllib2
import os
if __name__ == '__main__':
    url = os.environ['SLACK_URL']
    message = sys.argv[1]
    title = ("New Incoming Message")
    slack_data = {
        "attachments": [
            {
             "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    #byte_length = str(sys.getsizeof(slack_data))
    #headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    #response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    req = urllib2.Request(url, data=json.dumps(slack_data))
    try:
       response = urllib2.urlopen(req)
    except:
       print("Error sending message to Slack.Check if Slack Webhok URL is correct")
       sys.exit(1)
    
#Reference: https://medium.com/@sharan.aadarsh/sending-notification-to-slack-using-python-8b71d4f622f3
