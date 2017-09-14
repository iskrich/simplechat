import socket
import datetime
#maybe need extend
buffer_size = 1024
port = 1111

class SimpleChatServer:
    def __init__(self):
        #start server socket
        print("Starting server on localhost:%d" % port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))
        self.socket.listen(100)
        self.currentUsers = {}
        
    def start(self):
        while True:

            connect, address = self.socket.accept()
            msg = connect.recv(buffer_size)

            if address not in (x["address"] for x in self.currentUsers):
                self.currentUsers[address] = {"nickname": msg, "socket": connect}
                connect.send("Welcome to chat %s\n" % msg)
                msg = "%s connected to chat\n" % msg
            else:
                now = datetime.datetime.now()
                msg = "[%d:%d:%d] %s: %s" % (now.hour, now.minute, now.second,
                                             self.currentUsers[address]["nickname"], msg)
            for user in self.currentUsers.itervalues():
                user["socket"].send(msg + "\n")
            print(msg)

if __name__ == "__main__":
    server = SimpleChatServer()
    server.start()
