import socket

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1", 12345)
    client_socket.connect(server_address)

    try:
        message = input("enter a message: ")
        client_socket.sendall(message.encode())

        data = client_socket.recv(1024)

        print("Message received:", data.decode())

    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()