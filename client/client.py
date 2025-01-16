import socket

SERVER_IP = '101.101.1.2'  # Replace with your Raspberry Pi's IP
SERVER_PORT = 12345


def get_gpio_states():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((SERVER_IP, SERVER_PORT))
            client.sendall('GET_STATES'.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f'GPIO States: {response}')
            return response
    except Exception as e:
        print(f'An error occurred: {e}')
        return None


if __name__ == '__main__':
    states = get_gpio_states()
    print(states)
