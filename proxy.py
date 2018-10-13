from socket import socket
from inspect import isfunction
from pickle import dump, load

def rmi(cls, host, port):
    def resolver(proxy, name):
        def resolve(*args, **kwargs):
            dump((name, args, kwargs), proxy.wfile)
            return load(proxy.rfile)
        return resolve

    class Proxy:
        def __init__(self, *args, **kwargs):
            self.socket = socket()
            self.socket.connect((host, port))
            self.rfile = self.socket.makefile('rb', 0)
            self.wfile = self.socket.makefile('wb', 0)

            dump((cls.__module__, cls.__name__, args, kwargs), self.wfile)
            self.rfile.readline()

        def __getattribute__(self, name):
            try:
                # We are looking for Proxy instance attributes, i.e. socket
                return super(Proxy, self).__getattribute__(name)
            except AttributeError:
                # We are looking for cls attributes
                x = cls.__dict__[name]
                r = resolver(self, name)
                return r if isfunction(x) else r()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.socket.__exit__(*args)

    return Proxy
