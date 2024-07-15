import json
import boto3
import string
import random

dynamodb_client=boto3.client('dynamodb')
table_name='busBooking'

def generate_booking_id():
    return ''.join(random.choices(string.digits, k=10))

def lambda_handler(event, context):
    print(f"Input agent{event}")
    journey_date=event['parameters'][0]['value']
    destination=event['parameters'][1]['value']
    bus_id=event['parameters'][2]['value']
    source=event['parameters'][3]['value']
   
    booking_id = generate_booking_id()
    
    record = {
    'bookingID': {'N': str(booking_id)},
    'busId': {'N': bus_id},  
    'journeyDate': {'S': journey_date}, 
    'sourceCity': {'S': source},  
    'destinationCity': {'S': destination} 
    }
    
    try:
        response = dynamodb_client.put_item(TableName=table_name,Item=record)
        print(f"Record inserted successfully: {response}")  
        response_body = {
        'application/json': {
            'bookingID': f"Your ticket is booked successfully and your booking id is {booking_id}."
        }
    }
    except Exception as e:
        print(f"Error inserting record: {e}")
        response_body = {
        'application/json': {
            'bookingError': "Error encountered while booking your ticket. Try again later"
        }
    }
        
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    api_response = {
        'messageVersion': '1.0', 
        'response': action_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
        
    return api_response

