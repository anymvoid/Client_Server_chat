TCP Multiclient Chat (with Error Handling and Request Counter)
📚 Description
This project implements a TCP multiclient text chat, where:

Clients connect to a TCP server.

They can send messages that are forwarded to all other connected clients.

The server manages multiple simultaneous connections using threads.

Error handling is included during connection, sending, and receiving data.

The server keeps track of the number of messages received.

✅ Technologies: Python 3, socket, threading
✅ Communication type: TCP (connection-oriented / reliable)

🛠️ Features
Multiclient chat: each client can send messages that are shared with all other connected clients.

Separate threads: each client is managed in its own dedicated thread.

Error handling: closed connections or unexpected errors are handled using try-except blocks.

Request counter: the server keeps track of the total number of received messages.
