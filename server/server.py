import RPi.GPIO as GPIO
import socket
import threading
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setwarnings(False)
GPIO_PIN = 17
GPIO.setup(GPIO_PIN, GPIO.IN)

# Server setup
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 12345  # Define your desired port

clients = []

def handle_client(conn, addr):
    print(f"Client connected: {addr}")
    try:
        while True:
            data = conn.recv(1024)  # Keep the connection open
            if not data:
                break
    except Exception as e:
        print(f"Connection error with {addr}: {e}")
    finally:
        print(f"Client disconnected: {addr}")
        clients.remove(conn)
        conn.close()

# Function to broadcast messages to all clients
def broadcast(message):
    for conn in clients:
        try:
            conn.sendall(message.encode("utf-8"))
        except Exception as e:
            print(f"Failed to send message to a client: {e}")

# Start the server in a separate thread
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Server started on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr)).start()

# GPIO monitoring function
def monitor_gpio():
    print("Monitoring GPIO pin 17 for state changes...")
    last_state = GPIO.input(GPIO_PIN)

    while True:
        current_state = GPIO.input(GPIO_PIN)
        if current_state != last_state:
            state_str = "HIGH" if current_state else "LOW"
            message = f"GPIO pin 17 changed to {state_str}"
            print(message)
            broadcast(message)  # Broadcast the state change to clients
            last_state = current_state
        time.sleep(0.1)  # Poll every 100ms

# Main function
if __name__ == "__main__":
    try:
        threading.Thread(target=start_server, daemon=True).start()  # Start server
        monitor_gpio()  # Monitor GPIO
    except KeyboardInterrupt:
        print("\nExiting gracefully. Cleaning up GPIO...")
        GPIO.cleanup()
        for client in clients:
            client.close()
