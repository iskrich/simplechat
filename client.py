import socket
import os

from threading import Thread

from params import buffer_size, port, host


class SimpleChatUser:
    def __init__(self):
        self.nickname = ""
        self.connected = True
        self.socket = None

    def recieve_msg(self):
        while self.connected:
            try:
                data = self.socket.recv(buffer_size)
            except socket.timeout:
                continue
            if data:
                print data[:-1]

    def send_msg(self):
        while self.connected:
            msg = raw_input()
            if msg.strip() == "exit":
                self.connected = False
                self.socket.close()
                break
            else:
                self.socket.send(msg)

    def enter_chat(self):

        while 1:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.socket.settimeout(2)

            self.nickname = raw_input("Enter your name: ")
            self.socket.send(self.nickname)

            response = self.socket.recv(buffer_size)
            if response == "Fail_Nick":
                print("Nickname %s already used, please try again" % self.nickname)
                self.socket.close()
            else:
                print(response)
                break

        Thread(target=self.send_msg, args=()).start()
        Thread(target=self.recieve_msg, args=()).start()


if __name__ == "__main__":
    user = SimpleChatUser()
    user.enter_chat()
