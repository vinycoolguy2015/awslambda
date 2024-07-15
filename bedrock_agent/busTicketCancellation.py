import json
import boto3

dynamodb_client=boto3.client('dynamodb')
table_name='busBooking'

def lambda_handler(event, context):
    booking_id=event['parameters'][0]['value']

    try:
        response = dynamodb_client.delete_item(
            TableName=table_name,
            Key={
                'bookingID': {'N': str(booking_id)}
            }
        )
        print(f"Record with bookingID {booking_id} deleted successfully: {response}")
        response_body = {
        'application/json': {
            'bookingID': f"Your ticket with booking id {booking_id} cancelled successfully."
        }
    }
    except Exception as e:
        print(f"Error deleting record with bookingID {booking_id}: {e}")
        response_body = {
        'application/json': {
            'bookingError': "Error encountered while cancelling your ticket. Try again later"
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

