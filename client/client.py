import socket
import json

class ConnectionObject:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = None
        self._connect()

    def _connect(self):
        """Establish a persistent connection to the server."""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.ip, self.port))
            print(f"Connected to {self.ip}:{self.port}")
        except Exception as e:
            print(f"Error while connecting: {e}")
            self.client = None

    def get_gpio_states(self):
        """Send a request and receive the response using the persistent connection."""
        if not self.client:
            print("No active connection to the server.")
            return None
        try:
            self.client.sendall('GET_STATES'.encode('utf-8'))
            response = self.client.recv(1024).decode('utf-8')
            return json.loads(response)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def close(self):
        """Close the persistent connection."""
        if self.client:
            self.client.close()
            print("Connection closed.")
            self.client = None


def main(args):
    SERVER_IP = args.ip
    SERVER_PORT = args.port

    connector = ConnectionObject(SERVER_IP, SERVER_PORT)

    try:
        print(f"Received: {connector.get_gpio_states()}")
        # Add other requests or logic here if needed.
    finally:
        connector.close()
