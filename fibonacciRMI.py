from socket import socket
from pickle import dumps, loads

class Fibonacci:

    HOST = "localhost"
    PORT = 1234

    def calc(self, a):
        with socket() as soc:
            soc.connect((self.HOST, self.PORT))
            soc.sendall(dumps(a))
            return loads(soc.recv(4096))
