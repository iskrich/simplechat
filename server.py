import socket
import errno
import datetime
#maybe need extend
buffer_size = 1024
port = 1111

class SimpleChatServer:
    def __init__(self):
        #start server socket
        print("Starting server on localhost:%d" % port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.bind(('localhost', port))
        self.socket.listen(100)
        self.currentUsers = {}

    def _processNewUsers(self):
        connect, address = self.socket.accept()
        msg = connect.recv(buffer_size)

        if address not in self.currentUsers:
            self.currentUsers[address] = {"nickname": msg, "socket": connect}
            connect.send("Welcome to chat %s, type 'exit' for leaving from chat\n" % msg)
            self._broadcast(msg, "Connected to chat")

    def _listenUsers(self):
        for user in self.currentUsers.itervalues():
            s = user["socket"]
            data = s.recv(buffer_size)
            if data:
                self._broadcast(user["nickname"], data)

    def _broadcast(self, nick, msg):
        now = datetime.datetime.now()
        msg = "[%d:%d:%d] %s: %s" % (now.hour, now.minute, now.second,
                                     nick, msg)
        for adr in self.currentUsers.keys():
            try:
                self.currentUsers[adr]["socket"].send(msg + "\n")
            except socket.error as er:
                if er.errno == errno.WSAECONNRESET:
                    self.currentUsers[adr].close()
                    del self.currentUsers[adr]
        print(msg)

    def start(self):
        while True:
            self._listenUsers()
            self._processNewUsers()



if __name__ == "__main__":
    server = SimpleChatServer()
    server.start()
