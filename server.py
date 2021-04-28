from os import system
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, gethostbyname
from sys import exit
from threading import Thread


class ChatServer:
    audience_list = []
    latest_msg = ""

    def __init__(self):
        self.socket_fd = None
        self.listener()

    def listener(self):
        self.socket_fd = socket(AF_INET, SOCK_STREAM)
        self.socket_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket_fd.bind((gethostbyname('localhost'), 10000))
        print("Listener activated. Awaiting connections..")
        Thread(target=lambda script: system(f"python3 {script}"), args=["chat_box.py"]).start()
        self.socket_fd.listen(5)
        self.threaded_message()

    def receiver_list(self, client):
        if client not in self.audience_list:
            self.audience_list.append(client)

    def receive_messages(self, so):
        while True:
            try:
                message_buff = so.recv(256)
                # empty messages will not be delivered to the receiver
                msg_checker = (message_buff.decode("utf-8")).split(':')[-1]
                if not message_buff or len(msg_checker) < 2:
                    break
                self.latest_msg = message_buff.decode('utf-8')
                self.show_to_audience(so)  # send to all clients
            except OSError as os_error:
                if str(os_error) == '[Errno 9] Bad file descriptor':
                    print(f"Origin: {':'.join(str(raddr) for raddr in so.getsockname())} "
                          f"has been attempted to access from an unsupported gateway. "
                          f"Socket: {':'.join(str(raddr) for raddr in so.getpeername())}")
            except (KeyboardInterrupt, ConnectionResetError):
                exit("Thanks for using my chat server. Bye..")
        so.close()

    def show_to_audience(self, senders_socket):
        for client in self.audience_list:
            so, _ = client
            if so is not senders_socket:
                so.sendall(self.latest_msg.encode('utf-8'))

    def threaded_message(self):
        while True:
            try:
                client = so, (ip, port) = self.socket_fd.accept()
                self.receiver_list(client)
                print(f'Connection accepted from {ip}:{port}')
                Thread(target=self.receive_messages, args=([so])).start()
            except KeyboardInterrupt:
                exit("Thanks for using my chat server. Bye..")


if __name__ == "__main__":
    ChatServer()
