import socket

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
        self.currentUsers = []
        
    def start(self):
        while True:
            connect, adress = self.socket.accept()
            msg = connect.recvfrom(buffer_size)
            print msg
            print adress

server = SimpleChatServer()
server.start()
