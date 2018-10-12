from socket import socket
from inspect import isfunction
from pickle import dumps, loads

def rmi(cls, host, port):
    def resolver(socket):
        def resolve(*args, **kwargs):
            socket.sendall(dumps((args, kwargs)))
            return loads(socket.recv(4096))
        return resolve

    class Proxy:
        def __init__(self, *args, **kwargs):
            self.socket = socket()
            self.socket.connect((host, port))
            self.socket.sendall(dumps((args, kwargs)))
            self.socket.recv(4096)

        def __getattribute__(self, name):
            try:
                # We are looking for Proxy instance attributes, i.e. socket
                return super(Proxy, self).__getattribute__(name)
            except AttributeError:
                # We are looking for cls attributes
                x = cls.__dict__[name]
                r = resolver(self.socket)
                if isfunction(x):
                    return r
                else:
                    return r()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.socket.__exit__(*args)

    return Proxy
