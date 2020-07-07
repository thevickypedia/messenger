import socket
import threading


class ChatServer:
    audience_list = []
    latest_msg = ""

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
        self.threaded_message()

    def receiver_list(self, client):
        if client not in self.audience_list:
            self.audience_list.append(client)

    def receive_messages(self, so):
        while True:
            message_buff = so.recv(256)
            # empty messages will not be delivered to the receiver
            msg_checker = (message_buff.decode("utf-8")).split(':')[-1]
            if not message_buff or len(msg_checker) < 2:
                break
            self.latest_msg = message_buff.decode('utf-8')
            self.show_to_audience(so)  # send to all clients
        so.close()

    def show_to_audience(self, senders_socket):
        for client in self.audience_list:
            so, (ip, port) = client
            if so is not senders_socket:
                so.sendall(self.latest_msg.encode('utf-8'))

    def threaded_message(self):
        while True:
            try:
                client = so, (ip, port) = self.socket_fd.accept()
                self.receiver_list(client)
                print(f'Connection accepted from {ip}:{str(port)}')
                thread = threading.Thread(target=self.receive_messages, args=(so,))
                thread.start()
            except KeyboardInterrupt:
                print("Thanks for using Vignesh's chat server. Bye..")
                exit(0)


if __name__ == "__main__":
    ChatServer()
