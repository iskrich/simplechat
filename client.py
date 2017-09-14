import socket
import select
import os

from threading import Thread

from params import buffer_size, port, host

class SimpleChatUser:
    def __init__(self):
        self.nickname = ""
        self.connected = True
        self.socket = None

    def recieveMsg(self):
        while self.connected:
            sockets = [self.socket]
            reads, writes, errors = select.select(sockets, [], [])
            for s in reads:
                try:
                    if s == self.socket:
                        msg = s.recv(buffer_size)
                        if not msg:
                            os._exit(0)
                        else:
                            # delete last newline character
                            print(msg[:-1])
                except Exception as e:
                    print(e.message)
                    os._exit(0)

    def sendMsg(self):
        while self.connected:
            msg = raw_input()
            if msg.strip() == "exit":
                os._exit(0)
                break
            else:
                self.socket.send(msg)

    def enterChat(self):

        while 1:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.nickname = raw_input("Enter your name: ")
            self.socket.send(self.nickname)

            response = self.socket.recv(buffer_size)
            if response == "Fail_Nick":
                print("Nickname %s already used, please try again" % self.nickname)
                self.socket.close()
            else:
                print(response)
                break

        Thread(target=self.sendMsg, args=()).start()
        Thread(target=self.recieveMsg, args=()).start()


if __name__ == "__main__":
    user = SimpleChatUser()
    user.enterChat()
