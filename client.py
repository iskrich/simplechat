import socket

class SimpleChatUser:
    def __init__(self, nickname):
        self.nickname = nickname
        #connect to server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 1111))

    def enterChat(self):
        self.socket.send(self.nickname)

    def exitChat(self):
        self.socket.close()
        
if __name__ == "__main__":
    user = SimpleChatUser("Alice")
    user.enterChat()
    user.exitChat()
