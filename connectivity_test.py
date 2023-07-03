import json
import socket
def lambda_handler(event, context):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    hostname = "google.com"
    port = 443
    server_address = (hostname, port) # Server address and port
    try:
      IPAddr = socket.gethostbyname(hostname)
      print("Hostname: " + hostname)
      print("Host IP:" + IPAddr)
      print("Attempting to connect ..")
      sock.connect(server_address)
      sock.shutdown(socket.SHUT_RDWR)
      print("connected")
    except Exception as e:
      print("-- Error --")
      print(e)
    finally:
      sock.close()
