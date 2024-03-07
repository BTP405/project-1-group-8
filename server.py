"""Implement a simple client-server application where the server echoes back any message sent by a client. Use multi-threading to handle multiple client connections concurrently.

Requirements:

The server should be able to handle multiple client connections simultaneously using threads.
Each client should be able to send a message to the server.
The server should echo back the received message to the client.
Clients should be able to disconnect gracefully."""

import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        client_socket.send(data)  # Echo back the received message
    client_socket.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.01", 12345)
    server_socket.bind(server_address)
    server_socket.listen(1)
    
    print("server listening....")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, ))
        client_thread.start()




if __name__ == "__main__":
    run_server()