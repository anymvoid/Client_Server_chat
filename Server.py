import socket
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext

class ServerGUI:
    def __init__(self, master, HOST, PORT):
        self.master = master
        master.title("Server Chat")

        self.HOST = HOST
        self.PORT = PORT

        self.chat_area = scrolledtext.ScrolledText(master, width=50, height=25, state=tk.DISABLED)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_entry = tk.Entry(master, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5)

        self.send_button = tk.Button(master, text="Invia", width=10, command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        self.clients = []
        self.message_count = 0

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.HOST, self.PORT))
            self.server_socket.listen()
            self.log("Server in attesa di connessioni...")
            Thread(target=self.accept_clients).start()
        except Exception as e:
            self.log(f"Errore durante l'avvio del server: {e}")

    def log(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def display_message(self, sender, message, is_server=False):
        self.chat_area.config(state=tk.NORMAL)
        tag = "server" if is_server else "client"
        self.chat_area.insert(tk.END, f"{sender}: ", tag)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.tag_config(tag, font=("Arial", 10, "bold"))
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def accept_clients(self):
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                client_name = f"{address[0]}:{address[1]}"
                self.log(f"Connesso con {client_name}")
                self.clients.append((client_socket, client_name))
                Thread(target=self.talk_to_client, args=(client_socket, client_name)).start()
            except Exception as e:
                self.log(f"Errore accettando un client: {e}")
                break

    def talk_to_client(self, client_socket, client_name):
        Thread(target=self.receive_message, args=(client_socket, client_name)).start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            full_message = message  # Il prefisso "Server:" verrà aggiunto nella broadcast
            self.display_message("Server", full_message, is_server=True)
            self.broadcast(f"Server: {full_message}")
            self.message_entry.delete(0, tk.END)

    def receive_message(self, client_socket, client_name):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message or message.strip().lower() == "exit":
                    self.log(f"{client_name} disconnesso.")
                    # Rimuovi il client dalla lista
                    self.clients = [c for c in self.clients if c[0] != client_socket]
                    client_socket.close()
                    break
                self.message_count += 1
                formatted_message = message
                self.display_message(client_name, formatted_message)
                self.broadcast(f"{client_name}: {formatted_message}", sender=client_socket)
            except Exception as e:
                self.log(f"Errore ricevendo messaggio da {client_name}: {e}")
                # Rimuovi il client dalla lista in caso di errore
                self.clients = [c for c in self.clients if c[0] != client_socket]
                client_socket.close()
                break

    def broadcast(self, message, sender=None):
        for client_socket, _ in self.clients:
            if client_socket != sender:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    self.log(f"Errore inviando a un client: {e}")
                    # Rimuovi il client in caso di errore di invio
                    self.clients = [c for c in self.clients if c[0] != client_socket]
                    client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    server_gui = ServerGUI(root, '127.0.0.1', 7632)
    root.mainloop()