import socket


class ChatServer:
    def __init__(self):
        self.socket_fd = None
        self.listener()

    def listener(self):
        self.socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = '127.0.0.1'
        server_port = 10000
        self.socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_fd.bind((server_ip, server_port))
        print("Listener activated. Awaiting connections..")
        self.socket_fd.listen(5)


if __name__ == "__main__":
    ChatServer()
