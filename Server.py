import socket
import threading

# Server configuration
HOST = '0.0.0.0'
PORT = 5555

# List to store connected clients
clients = []

def handle_client(client_socket, username):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            broadcast(f"{username}: {message}")

    except Exception as e:
        print(f"Error handling client {username}: {e}")

    finally:
        remove_client(client_socket)

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode())
        except Exception as e:
            print(f"Error broadcasting message: {e}")

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            username = client_socket.recv(1024).decode()
            clients.append(client_socket)

            client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
            client_handler.start()

    except Exception as e:
        print(f"Error in server: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
