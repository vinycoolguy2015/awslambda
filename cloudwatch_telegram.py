import json
import urllib3
def lambda_handler(event, context):
    
    
    instance_id=event['detail']['configuration']['metrics'][0]['metricStat']['metric']['dimensions']['InstanceId']
    bot_token = '<yourtoken>'
    bot_chatID = '<chatid>'
    message=instance_id + " breached CPU utilization threshold."
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
    
    http = urllib3.PoolManager()
    response = http.request("GET", send_text)
    return (response.status)
