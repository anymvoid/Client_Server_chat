import socket
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext
import os

class ClientGUI:
    def __init__(self, master, HOST, PORT):
        self.master = master
        master.title("Chat")  # Titolo più generico

        self.HOST = HOST
        self.PORT = PORT

        self.chat_area = scrolledtext.ScrolledText(master, width=50, height=25, state=tk.DISABLED)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_entry = tk.Entry(master, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5)

        self.send_button = tk.Button(master, text="Invia", width=10, command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        try:
            self.client_socket = socket.socket()
            self.client_socket.connect((self.HOST, self.PORT))
            self.log("Connesso al server.")
            Thread(target=self.receive_message).start()
        except Exception as e:
            self.log(f"Errore connettendosi al server: {e}")
            os._exit(0)

    def log(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n", "server_message")
        self.chat_area.tag_config("server_message", foreground="green") # Evidenzia i messaggi del server
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def display_message(self, sender, message, is_local=False):
        self.chat_area.config(state=tk.NORMAL)
        tag = "local" if is_local else "remote"
        self.chat_area.insert(tk.END, f"{sender}: ", tag)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.tag_config(tag, font=("Arial", 10, "bold"))
        if is_local:
            self.chat_area.tag_config(tag, foreground="blue") # Evidenzia i messaggi locali
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def send_message(self):
        client_message = self.message_entry.get()
        if client_message:
            try:
                self.client_socket.send(client_message.encode())
                self.display_message("Tu", client_message, is_local=True)
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.log(f"Errore inviando messaggio: {e}")
                self.close_connection()

    def receive_message(self):
        while True:
            try:
                server_message = self.client_socket.recv(1024).decode()
                if not server_message:
                    self.log("Server disconnesso.")
                    self.close_connection()
                    break
                sender, content = server_message.split(":", 1)
                self.display_message(sender.strip(), content.strip())
            except Exception as e:
                self.log(f"Errore ricevendo messaggio: {e}")
                self.close_connection()
                break

    def close_connection(self):
        try:
            self.client_socket.close()
        except OSError:
            pass
        os._exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    client_gui = ClientGUI(root, '127.0.0.1', 7632)
    root.mainloop()