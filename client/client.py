import socket

SERVER_IP = '101.101.1.2'
SERVER_PORT = 12345

try:
    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, SERVER_PORT))
        print("Connected to the server. Listening for messages...\n")

        while True:
            # Receive and print data from the server
            data = client.recv(1024).decode("utf-8")
            if data:
                print(f"Received: {data}")
            else:
                break
except KeyboardInterrupt:
    print("\nDisconnected from the server.")
except Exception as e:
    print(f"An error occurred: {e}")
