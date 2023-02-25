#python sendRequest.py 'APIGatewayURL'

import sys
import requests

def send_request(url):
    response = requests.get(url)
    return response

def send_request_with_token(url, id_token):
    response = requests.get(url, headers={'Authorization': id_token})
    return response

if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            print("Sending your request WITHOUT id token generated by Cognito.....")
            #send request without id_token
            response = send_request(sys.argv[1])
            print("Response code: {} , Response Data: {}".format(response.status_code, response.text))
        except Exception as e:
            print(e)
    elif len(sys.argv) == 3:
        try:
            print("Sending your request WITH id token generated by Cognito.....\n")
            #send request with id_token
            response = send_request_with_token(sys.argv[1], sys.argv[2])
            if response.status_code == 401:
                print("Please check if your ID token is valid or it may be expired. You may regenerate your ID token using getJWT.py")
            else:
                print("Response code: {} , Response Data: {}".format(response.status_code, response.text))
        except Exception as e:
            print(e)
    else:
        print(" Please check your inputs.\n example) python sendRequest.py <URL> <ID_Token>")
