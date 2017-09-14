import socket
import select
import sys
from threading import Thread

from server import buffer_size, port

class SimpleChatUser:
    def __init__(self, nickname):
        self.nickname = nickname
        #connect to server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', port))
        self.connected = True

    def recieveMsg(self):
        while self.connected:
            sockets = [self.socket]
            reads, writes, errors = select.select(sockets, [], [])
            for s in reads:
                if s == self.socket:
                    newMsg = s.recv(buffer_size)
                    if not newMsg:
                        sys.exit()
                    else:
                        print(newMsg)

    def sendMsg(self):
        while self.connected:
            msg = raw_input(">")
            if msg.strip() == "exit":
                self.socket.close()
                self.connected = False
                break
            self.socket.send(msg)

    def enterChat(self):
        self.nickname = raw_input("Enter your name: ")
        self.socket.send(self.nickname)
        Thread(target=self.sendMsg, args=()).start()
        Thread(target=self.recieveMsg, args=()).start()

    def exitChat(self):
        self.socket.close()

if __name__ == "__main__":
    user = SimpleChatUser("Alice")
    user.enterChat()
