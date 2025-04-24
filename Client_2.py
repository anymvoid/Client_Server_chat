import socket
import threading

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(msg)
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

thread = threading.Thread(target=receive, args=(client,))
thread.start()

while True:
    msg = input()
    client.send(msg.encode())