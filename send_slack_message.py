import json
import sys
import random
import urllib2
if __name__ == '__main__':
    url = ""
    message = ("Python 2.7")
    title = ("New Message")
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
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    req = urllib2.Request(url, data=json.dumps(slack_data))
    response = urllib2.urlopen(req)
    result = response.read()
    print(result)
    
#Reference: https://medium.com/@sharan.aadarsh/sending-notification-to-slack-using-python-8b71d4f622f3
