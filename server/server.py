def main(args):
    def handle_client(conn, addr):
        print(f'Client connected: {addr}')
        try:
            while True:
                data = conn.recv(1024)  # Receive data from the client
                if not data:
                    break
                request = data.decode('utf-8').strip()
                if request == 'GET_STATES':
                    states = {pin: 'HIGH' if GPIO.input(pin) else 'LOW' for pin in GPIO_PINS}
                    response = json.dumps(states)
                    conn.sendall(response.encode('utf-8'))
                else:
                    conn.sendall('Invalid request'.encode('utf-8'))
        except Exception as e:
            print(f'Connection error with {addr}: {e}')
        finally:
            print(f'Client disconnected: {addr}')
            clients.remove(conn)
            conn.close()

    # Start the server in a separate thread
    def start_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(5)
            print(f'Server started on {HOST}:{PORT}')
            while True:
                conn, addr = server.accept()
                clients.append(conn)
                threading.Thread(target=handle_client, args=(conn, addr)).start()

    # Main function
    import json
    import socket
    import threading

    import RPi.GPIO as GPIO

    # GPIO setup
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
    GPIO.setwarnings(False)
    GPIO_PINS = [17, 27, 22]
    for pin in GPIO_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Server setup
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 12345  # Define your desired port

    clients = []
    try:
        # Start server
        start_server()
    except KeyboardInterrupt:
        print('\nExiting gracefully. Cleaning up GPIO...')
        GPIO.cleanup()
        for client in clients:
            client.close()


if __name__ == '__main__':
    main(None)
