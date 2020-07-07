import socket


class ChatBox:
    user_socket = None

    def __init__(self):
        self.socket_init()

    def socket_init(self):
        self.user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user_ip = '127.0.0.1'
        user_port = 10000
        self.user_socket.connect((user_ip, user_port))


if __name__ == '__main__':
    ChatBox()
