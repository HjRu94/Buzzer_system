def get_gpio_states(SERVER_IP, SERVER_PORT):
    import socket
    import json
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((SERVER_IP, SERVER_PORT))
            client.sendall('GET_STATES'.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            return response
    except Exception as e:
        print(f'An error occurred: {e}')
        return None


def main(args):
    SERVER_IP = args.ip
    SERVER_PORT = args.port

    print(f'recieved: {get_gpio_states(SERVER_IP, SERVER_PORT)}')
