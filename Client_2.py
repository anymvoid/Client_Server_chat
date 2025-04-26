import socket
from threading import Thread
import os

class Client:
    def __init__(self, HOST, PORT):
        try:
            self.socket = socket.socket()
            self.socket.connect((HOST, PORT))
            print("Connesso al server.")
            self.talk_to_server()
        except Exception as e:
            print(f"Errore connettendosi al server: {e}")
            os._exit(0)

    def talk_to_server(self):
        Thread(target=self.receive_message).start()
        self.send_message()

    def send_message(self):
        while True:
            try:
                client_message = input("")
                self.socket.send(client_message.encode())
            except Exception as e:
                print(f"Errore inviando messaggio: {e}")
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
            except Exception as e:
                print(f"Errore ricevendo messaggio: {e}")
                self.socket.close()
                os._exit(0)

Client('127.0.0.1', 7632)
