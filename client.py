import socket

from threading import Thread

from params import buffer_size, port, host


class SimpleChatUser:
    """
    Client object, is designed to send and receive messages from server.
    Parameters for server (hostname, port, max_users) were in params.py
    """
    def __init__(self):
        self.nickname = ""
        self.connected = True
        self.socket = None
        self.history = []

    def recieve_msg(self):
        while self.connected:
            try:
                data = self.socket.recv(buffer_size)
            except socket.timeout:
                continue
            if data:
                self.history.append(data[:-1])
                print data[:-1]

    def send_msg(self):
        while self.connected:
            # user input
            msg = raw_input()
            if msg.strip() == "exit":
                # exit action
                self.exit()
                break
            else:
                # regular message
                self.socket.send(msg)

    def login(self, nickname):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        # when send_msg() generate exit, thread with receive_msg() will wait indefinitely time
        # That's why need limit waiting time.
        self.socket.settimeout(2)

        self.nickname = nickname
        self.socket.send(self.nickname)

        return self.socket.recv(buffer_size)

    def exit(self):
        # break loop, send to server and close socket
        self.connected = False
        self.socket.send("exit")
        self.socket.close()

    def enter_chat(self, name=""):
        while 1:
            if name == "":
                name = raw_input("Enter your name:")
            response = self.login(name)
            if response == "Fail_Nick":
                print("Nickname %s already used, please try again" % self.nickname)
                self.socket.close()
                name = ""
            else:
                print(response)
                break

        # Two main loop: for receive and send
        Thread(target=self.send_msg, args=()).start()
        Thread(target=self.recieve_msg, args=()).start()


if __name__ == "__main__":
    user = SimpleChatUser()
    user.enter_chat()
