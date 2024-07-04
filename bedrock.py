import json
import boto3
import re
from datetime import datetime
import zipfile
import os
import time

# Initialize AWS clients
lambda_client = boto3.client("lambda", region_name='us-east-1')
bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
s3 = boto3.client("s3", region_name='us-east-1')

def create_zip_file(zip_file_name, file_to_zip):
    """
    Create a zip file containing the given file.

    Parameters:
    - zip_file_name (str): Name of the zip file to create.
    - file_to_zip (str): Path to the file to include in the zip.
    """
    print(f"Creating zip file: {zip_file_name}")
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        zipf.write(file_to_zip, os.path.basename(file_to_zip))
    print(f"{zip_file_name} created successfully.")

def extract_code(response_text):
    """
    Extract Python code block from response text using regex.

    Parameters:
    - response_text (str): Text containing the Python code block.

    Returns:
    - str: Extracted Python code block.
    """
    match = re.search(r'```python\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1)
    return response_text  # Return the whole text if no code block is found

def save_code_to_s3(code, bucket, key_prefix='code-output'):
    """
    Save Python code to a temporary file and upload as a zip to S3.

    Parameters:
    - code (str): Python code to save.
    - bucket (str): S3 bucket name.
    - key_prefix (str): S3 key prefix (default: 'code-output').

    Returns:
    - str: S3 key where the zip file is uploaded.
    """
    current_time = datetime.now().strftime("%H%M%S")
    temp_file_path = f"/tmp/lambda_function.py"
    
    # Save code to a temporary file
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(code)
    
    # Create and upload zip file to S3
    zip_file_path = f"/tmp/{current_time}.zip"
    create_zip_file(zip_file_path, temp_file_path)
    
    s3_key = f"{key_prefix}/{current_time}.zip"
    s3.upload_file(zip_file_path, bucket, s3_key)
    print(f"Code saved to S3: s3://{bucket}/{s3_key}")
    
    return s3_key

def update_lambda_function(function_name, bucket, s3_key):
    """
    Update Lambda function code and wait until it becomes active.

    Parameters:
    - function_name (str): Name of the Lambda function to update.
    - bucket (str): S3 bucket name containing the code package.
    - s3_key (str): S3 key for the code package.

    Returns:
    - bool: True if function becomes active, False otherwise.
    """
    try:
        # Update Lambda function code
        lambda_client.update_function_code(
            FunctionName=function_name,
            S3Bucket=bucket,
            S3Key=s3_key,
            Publish=True
        )
        
        # Wait until Lambda function state is Active
        return wait_until_active(function_name)
    
    except Exception as e:
        print(f"Error updating Lambda function {function_name}: {e}")
        return False

def wait_until_active(function_name, max_attempts=30, wait_interval=10):
    """
    Wait until Lambda function state is Active.

    Parameters:
    - function_name (str): Name of the Lambda function to check.
    - max_attempts (int): Maximum number of attempts to check (default: 30).
    - wait_interval (int): Time interval in seconds between attempts (default: 10).

    Returns:
    - bool: True if function becomes active, False otherwise.
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            response = lambda_client.get_function(FunctionName=function_name)
            function_state = response['Configuration']['State']
            
            if function_state == 'Active':
                print(f"Lambda function {function_name} is active and ready.")
                return True
            
            print(f"Lambda function {function_name} is {function_state}. Waiting for activation...")
            time.sleep(wait_interval)
            attempts += 1
        
        except Exception as e:
            print(f"Error checking Lambda function state: {e}")
            time.sleep(wait_interval)
            attempts += 1
    
    print(f"Lambda function {function_name} did not become active within the specified time.")
    return False

def lambda_handler(event, context):
    try:
        if 'Prompt' not in event:
            raise ValueError("Prompt not provided")

        prompt = event['Prompt']

        # Call Bedrock Runtime to get Python code based on the prompt
        body = json.dumps({
            "prompt": f"Human: Write python code for the following instructions: {prompt}\\nAssistant:",
            "max_tokens_to_sample": 2048,
            "temperature": 0.1,
            "top_p": 0.2,
            "top_k": 250,
            "stop_sequences": ["\\n\\nHuman"]
        })

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId='anthropic.claude-v2',
            accept='application/json',
            contentType='application/json'
        )

        response_content = response["body"].read().decode("utf-8")
        response_data = json.loads(response_content)
        code = extract_code(response_data["completion"].strip())

        # Save code to S3 and update Lambda function
        s3_bucket = "<S3_BUCKET>"
        s3_key = save_code_to_s3(code, s3_bucket)
        
        if update_lambda_function('bedrock-test2', s3_bucket, s3_key):
            print("Lambda function code updated successfully.")
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': "Lambda function did not become active."
                })
            }

        # Invoke updated Lambda function
        response = lambda_client.invoke(FunctionName='bedrock-test2', InvocationType='RequestResponse')
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))

        return {
            'statusCode': 200,
            'body': json.dumps(response_payload)
        }

    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
