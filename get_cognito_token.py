import boto3
import sys
import hmac, hashlib, base64
from datetime import datetime

def get_id_token(region, username, password, user_pool_id, app_client_id, app_client_secret):
    client = boto3.client('cognito-idp', region_name=region)

    #SecretHash is required when a user pool app client is configured with a client secret in the user pool
    #https://aws.amazon.com/premiumsupport/knowledge-center/cognito-unable-to-verify-secret-hash/
    message = bytes(username+app_client_id,'utf-8')
    key = bytes(app_client_secret,'utf-8')
    secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()

    resp = client.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=app_client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": username,
            'SECRET_HASH': secret_hash,
            "PASSWORD": password
        }
    )

    #print("Access token:", resp['AuthenticationResult']['AccessToken'])
    print(" ID token:", resp['AuthenticationResult']['IdToken'])

if __name__ == "__main__":
    my_session = boto3.session.Session()
    region_name = my_session.region_name

    if len(sys.argv) == 6:
        now = datetime.now()
        # dd/mm/YY H:M:S
        now_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(" Getting your ID token that will be expired in 60 minutes... \n Current time: " + now_string + "\n")

        #username, password, user_pool_id, app_client_id, app_client_secret
        try:
            id_token = get_id_token(region_name, sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4],sys.argv[5])
        except Exception as e:
            print(e)
    else:
        print(" \n Please refer to the following format. \n python getIDtoken.py <username> <user_password> <user_pool_id> <app_client_id> <app_client_secret> ")
