import socket
from threading import Thread
import os

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.talk_to_server()

    def talk_to_server(self):
        Thread(target=self.receive_message).start()
        self.send_message()

    def send_message(self):
        while True:
            try:
                client_message = input("")
                self.socket.send(client_message.encode())
            except:
                self.socket.close()
                os._exit(0)

    def receive_message(self):
        while True:
            try:
                server_message = self.socket.recv(1024).decode()
                if not server_message:
                    print("Server disconnesso.")
                    self.socket.close()
                    os._exit(0)
                print("\033[1;32;40m" + server_message + "\033[0m")
            except:
                self.socket.close()
                os._exit(0)

Client('127.0.0.1', 7632)
