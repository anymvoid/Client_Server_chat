import socket
from threading import Thread
import os

class Server:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        print('Server in attesa di connessioni...')
        self.clients = []

        self.accept_clients()

    def accept_clients(self):
        while True:
            client_socket, address = self.socket.accept()
            print(f"Connesso con {address}")
            self.clients.append(client_socket)
            Thread(target=self.talk_to_client, args=(client_socket, address)).start()

    def talk_to_client(self, client_socket, address):
        Thread(target=self.receive_message, args=(client_socket, address)).start()
        self.send_message(client_socket, address)

    def send_message(self, client_socket, address):
        while True:
            try:
                message = input("")
                self.broadcast(f"Server: {message}")
            except:
                client_socket.close()
                self.clients.remove(client_socket)
                break

    def receive_message(self, client_socket, address):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message or message.strip().lower() == "exit":
                    print(f"{address} disconnesso.")
                    client_socket.close()
                    self.clients.remove(client_socket)
                    break
                print(f"\033[1;31;40m{address}: {message}\033[0m")
                self.broadcast(f"{address}: {message}", sender=client_socket)
            except:
                client_socket.close()
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
                break

    def broadcast(self, message, sender=None):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    self.clients.remove(client)

Server('127.0.0.1', 7632)
