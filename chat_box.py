import os
from socket import socket, AF_INET, SOCK_STREAM, gethostbyname
from threading import Thread
from time import sleep
from tkinter import Tk, END, Frame, Text, Scrollbar, Label, Entry, Button, VERTICAL, messagebox


class ChatBox:
    user_socket = None
    latest_msg = None

    def __init__(self, master):
        self.core = master
        self.transcript_box = None
        self.name_box = None
        self.text_box = None
        self.join_button = None
        self.socket_init()
        self.chatbox_init()
        self.message_listener()

    def socket_init(self):
        self.user_socket = socket(AF_INET, SOCK_STREAM)
        self.user_socket.connect((gethostbyname('localhost'), 10000))

    def chatbox_init(self):
        self.core.title("Socket Chat")
        self.core.resizable(0, 0)
        self.chat_box()
        self.display_name_section()
        self.chat_area()

    def message_listener(self):
        Thread(target=self.msg_from_server, args=([self.user_socket])).start()

    def msg_from_server(self, so):
        while True:
            size = so.recv(256)
            if not size:
                break
            message = size.decode('utf-8')
            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                self.transcript_box.insert('end', message + '\n')
                self.transcript_box.yview(END)
            else:
                self.transcript_box.insert('end', message + '\n')
                self.transcript_box.yview(END)

        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Enter your Name:', font=("Times", 16)).pack(side='left', padx=10)
        self.name_box = Entry(frame, width=50, borderwidth=2)
        self.name_box.pack(side='left', anchor='e')
        self.join_button = Button(frame, text="Join", width=10, command=self.join_response).pack(side='left')
        frame.pack(side='top', anchor='nw')

    def chat_box(self):
        frame = Frame()
        Label(frame, text='Live Transcript', font=("Times", 12)).pack(side='top', anchor='w')
        self.transcript_box = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.transcript_box.yview, orient=VERTICAL)
        self.transcript_box.config(yscrollcommand=scrollbar.set)
        self.transcript_box.bind('<KeyPress>', lambda e: 'random')
        self.transcript_box.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def chat_area(self):
        frame = Frame()
        Label(frame, text='Message:', font=("Times", 12)).pack(side='top', anchor='w')
        self.text_box = Text(frame, width=60, height=3, font=("Serif", 12))
        self.text_box.pack(side='left', pady=15)
        self.text_box.bind('<Return>', self.enter_response)
        frame.pack(side='top')

    def join_response(self):
        if len(self.name_box.get()) == 0:
            messagebox.showerror(
                "Enter your name!", "Enter your name to join messenger")
            return
        self.name_box.config(state='disabled')
        self.user_socket.send(("joined:" + self.name_box.get()).encode('utf-8'))

    def enter_response(self, event):
        if len(self.name_box.get()) == 0:
            messagebox.showerror(
                "Enter your name!", "Enter your name to send a message!")
            return
        self.send_chat()
        self.remove_text()

    def remove_text(self):
        self.text_box.delete(1.0, 'end')

    def send_chat(self):
        sender = self.name_box.get().strip() + ": "
        data = self.text_box.get(1.0, 'end').strip()
        message = (sender + data).encode('utf-8')
        self.transcript_box.insert('end', message.decode('utf-8') + '\n')
        self.transcript_box.yview(END)
        self.user_socket.send(message)
        self.remove_text()
        return 'random'

    def close_response(self):
        if messagebox.askokcancel("Message from Chat Box", "Are you sue you want to leave?"):
            self.core.destroy()
            self.user_socket.close()
            # noinspection PyProtectedMember,PyUnresolvedReferences
            os._exit(0)  # using os to avoid OSError


if __name__ == '__main__':
    sleep(3)
    trigger = Tk()
    try:
        chat_win = ChatBox(trigger)
        trigger.protocol("WM_DELETE_WINDOW", chat_win.close_response)
        trigger.mainloop()
    except ConnectionRefusedError:
        print('Port 10000 is not actively listening. Please check and enable the server/listener.')
