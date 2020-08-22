import socket

class Server:
    def __init__(self):
        self.server=socket.socket()
        host=''
        port=9999
        self.server.bind((host,port))
        print('server is ready')
        self.server.listen(5)
        self.AcceptConnection()
    def AcceptConnection(self):
        while True:
            client,address=self.server.accept()
            client.send(bytes("Welcome!!", 'utf-8'))
s=Server()