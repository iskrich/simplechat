import socket
import errno
import datetime
import select
from params import buffer_size, host, port, max_users


class SimpleChatServer:
    def __init__(self):
        #start server socket
        print("Starting server on %s:%d" % (host, port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(max_users)
        self.currentUsers = {}
        self.currentUsers[self.socket] = "Server"

    def _processNewUsers(self):
        connect, address = self.socket.accept()
        nick = connect.recv(buffer_size)

        if nick in self.currentUsers.values():
            connect.send("Fail_Nick")
            return

        self.currentUsers[connect] = nick
        connect.send("Welcome to chat %s, type 'exit' for leaving from chat" % nick)
        self._broadcast(self.socket, "%s connected to chat" % nick)

    def _listenUsers(self):
        reads, writes, execs = select.select(self.currentUsers.keys(), [], [])

        for s in reads:
            if s is self.socket:
                self._processNewUsers()
            else:
                try:
                    msg = s.recv(buffer_size)
                    if msg:
                        self._broadcast(s, msg)
                except socket.error as er:
                    if er.errno == errno.WSAECONNRESET:
                        self._handleDisconnectedUser(s)

    def _broadcast(self, sock, msg):
        now = datetime.datetime.now()
        msg = "[%d:%d:%d] %s: %s" % (now.hour, now.minute, now.second,
                                     self.currentUsers[sock], msg)
        for s in self.currentUsers.keys():
            try:
                if s != self.socket:
                    s.send(msg + "\n")
            except socket.error as er:
                if er.errno == errno.WSAECONNRESET:
                    self._handleDisconnectedUser(s)
        print(msg)

    def _handleDisconnectedUser(self, sock):
        nickname = self.currentUsers[sock]
        del self.currentUsers[sock]
        self._broadcast(self.socket, "%s disconnected from chat" % nickname)

    def start(self):
        while True:
            self._listenUsers()


if __name__ == "__main__":
    server = SimpleChatServer()
    server.start()
