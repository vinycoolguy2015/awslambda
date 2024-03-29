import json
#import traceback
from datetime import datetime, timedelta
from botocore.vendored import requests
import boto3



def findVaccineSlotsAvailability(pinCodeList):    
    #Cowin URL
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode='
    client = boto3.client('sns',region_name='us-east-1')

    
    urls = list()
    for pin in pinCodeList:
        current = datetime.today().strftime('%d-%m-%Y')
        tempUrl = url + pin + "&date="
        for i in range(1,15):
            urls.append(tempUrl+current)
            next_week = datetime.today() + timedelta(days=i)
            current = next_week.strftime('%d-%m-%Y')

    #Set the below header, otherwise, you may get 403 error
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    slotFound = False
    #Create empty set to store the message to be sent
    message = set()
    message.add("Vaccine Alert:::::")

    for url in urls:
        response = requests.get(url, headers=headers)
        data=json.loads(response.text)
        
        for center in data['centers']:
            if 'sessions' in center:
                for session in center['sessions']:
                    message.add("Pincode:"+str(center["pincode"])+" Center Name:"+str(center["name"]+" Date:"+session["date"]+" Minimum Age:"+str(session["min_age_limit"])+" Dose1 Capacity:"+str(session["available_capacity_dose1"])+" Dose2 Capacity:"+str(session["available_capacity_dose2"])))
                    slotFound = True                
    if slotFound:
        client.publish(TargetArn="test",Message=str(message))        
    else:        
        print("No slot found.")
        
def lambda_handler(event, context):
    try:    
        pinCodeList=['xxxxxx']
        #Call the function with the desired pin code list
        findVaccineSlotsAvailability(pinCodeList)
        
        
    except Exception as e:
        #traceback.print_exc()
        print("Request errored out")
