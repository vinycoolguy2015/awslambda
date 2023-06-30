import socket

def ping(host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Set the timeout value for the connection

        # Connect to the host on the specified port
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open on {host}")
        else:
            print(f"Port {port} is closed on {host}")

        # Close the socket
        sock.close()

    except socket.error as e:
        print(f"Error: {e}")

def lambda_handler(event, context):
    # Usage example
    ping("google.com", 443)
