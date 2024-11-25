import boto3
import random
import json
from datetime import datetime
import time

# AWS Configuration
LOG_GROUP_NAME = "my-test-log-group-1"
LOG_STREAM_NAME = "my-test-log-stream-1"
REGION_NAME = "us-east-1"

# Initialize the boto3 CloudWatch Logs client
client = boto3.client('logs', region_name=REGION_NAME)

def get_current_timestamp():
    """Return the current timestamp in milliseconds."""
    return int(time.time() * 1000)

def create_log_event():
    """Create a log event with random level and current timestamp."""
    message = {
        "message": "incoming → GET / HTTP/1.1",
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")[:-3],
    }

    # Randomly decide whether to include the "level" field
    if random.choice([True, False]):
        message["level"] = random.choice(["info", "error"])
    
    return {
        'timestamp': get_current_timestamp(),
        'message': json.dumps(message)  # Serialize message as JSON
    }

def push_logs_to_cloudwatch():
    """Push 20,000 log events to a CloudWatch Logs stream."""
    try:
        # Retrieve the current sequence token
        response = client.describe_log_streams(
            logGroupName=LOG_GROUP_NAME,
            logStreamNamePrefix=LOG_STREAM_NAME
        )
        
        if not response['logStreams']:
            raise ValueError("Log stream not found")

        upload_sequence_token = response['logStreams'][0].get('uploadSequenceToken', None)

        # Generate log events
        log_events = [create_log_event() for _ in range(20000)]

        # Push logs in batches (CloudWatch has a limit of 1MB per request)
        batch_size = 100  # Customize the batch size as needed
        for i in range(0, len(log_events), batch_size):
            batch = log_events[i:i+batch_size]

            # Prepare the arguments for put_log_events
            kwargs = {
                "logGroupName": LOG_GROUP_NAME,
                "logStreamName": LOG_STREAM_NAME,
                "logEvents": batch,
            }
            if upload_sequence_token:  # Include sequenceToken only if it's available
                kwargs["sequenceToken"] = upload_sequence_token

            # Put log events into the CloudWatch log stream
            put_response = client.put_log_events(**kwargs)

            # Update sequence token for the next batch
            upload_sequence_token = put_response['nextSequenceToken']

            print(f"Pushed batch {i // batch_size + 1} to CloudWatch.")


    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    push_logs_to_cloudwatch()
