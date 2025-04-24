import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"{addr} connesso.")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg:
                print(f"{addr}: {msg}")
                broadcast(f"{addr}: {msg}", conn)
            else:
                break
        except:
            break
    conn.close()
    clients.remove(conn)
    print(f"{addr} disconnesso.")

def broadcast(msg, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(msg.encode())
            except:
                client.close()
                clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
server.listen()

print("Server multiclient avviato...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
