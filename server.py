import socket
import errno
import datetime
import select
from threading import Thread
from params import buffer_size, host, port, max_users


class SimpleChatServer(Thread):
    """Main server class, used for registrating and processing client sockets.
    Class is a successor of threading.Thread, as a result object start up in
    separated thread.
    Parameters for server (hostname, port, max_users) were in params.py
    """
    def __init__(self):
        print("Starting server on %s:%d" % (host, port))

        # create server socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(max_users)
        self.socket.settimeout(1)

        self.stopped = False

        self.currentUsers = {}

        # Server used like client for sending system messages
        self.currentUsers[self.socket] = "Server"

        Thread.__init__(self)

    def _process_new_users(self):
        connect, address = self.socket.accept()
        nick = connect.recv(buffer_size)

        if nick in self.currentUsers.values():
            connect.send("Fail_Nick")
            return

        self.currentUsers[connect] = nick
        connect.send("Welcome to chat %s, type 'exit' for leaving from chat" % nick)
        self._broadcast(self.socket, "%s connected to chat" % nick)

    def _listen_users(self):
        # collect all available sockets
        reads, writes, execs = select.select(self.currentUsers.keys(), [], [], 1)

        for s in reads:
            if s is self.socket:
                # server socket checking new connection
                self._process_new_users()
            else:
                try:
                    # read messages from current users
                    msg = s.recv(buffer_size)
                    if msg:
                        # user send exit action
                        if msg.strip() == "exit":
                            self._handle_disconnected_user(s)
                        else:
                            self._broadcast(s, msg)
                # case when user socket connection was terminated
                except socket.error as er:
                    if er.errno == errno.WSAECONNRESET:
                        self._handle_disconnected_user(s)

    def _broadcast(self, sock, msg):
        now = datetime.datetime.now()
        # message format -- [time] nick : message
        msg = "[%d:%d:%d] %s: %s" % (now.hour, now.minute, now.second,
                                     self.currentUsers[sock], msg)

        for s in self.currentUsers.keys():
            try:
                if s != self.socket:
                    s.send(msg + "\n")
            except socket.error as er:
                if er.errno == errno.WSAECONNRESET:
                    self._handle_disconnected_user(s)
        print(msg)

    def _handle_disconnected_user(self, sock):
        # delete user from current pool and alert others
        nickname = self.currentUsers[sock]
        del self.currentUsers[sock]
        self._broadcast(self.socket, "%s disconnected from chat" % nickname)

    def run(self):
        while not self.stopped:
            self._listen_users()

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    server = SimpleChatServer()
    server.start()
