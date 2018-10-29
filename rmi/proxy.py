from socket import socket
from inspect import  isfunction

from .interface import *
from .misc import PickleMixin

def stub(cls, host, port):
    def resolver(proxy, name):
        def resolve(*args, **kwargs):
            req = MethodRequest(name, args, kwargs)
            proxy.dump(req)
            resp = proxy.load()
            return resp.returnOrRaise()
        return resolve

    class Proxy(PickleMixin):
        def __init__(self, *args, **kwargs):
            self.socket = socket()
            self.socket.connect((host, port))
            self.rfile = self.socket.makefile("rb", 0)
            self.wfile = self.socket.makefile("wb", 0)

            # Remote instanciate class
            req = ClassRequest(cls.__module__, cls.__name__, args, kwargs)
            self.dump(req)
            resp = self.load()
            resp.returnOrRaise()

            # Prepare for attribute manipulation
            self.inited = True

        def __getattribute__(self, name):
            try:
                # We are looking for Proxy instance attributes, i.e. socket
                return super().__getattribute__(name)
            except AttributeError:
                # We are looking for cls attributes
                if name in cls.__dict__ and isfunction(cls.__dict__[name]):
                    # Remote invoke method later
                    r = resolver(self, name)
                    return r
                else:
                    # Get instance attribute now
                    req = GetAttributeRequest(name)
                    self.dump(req)
                    resp = self.load()
                    return resp.returnOrRaise()

        def __setattr__(self, name, value):
            try:
                self.__dict__["inited"]
                req = SetAttributeRequest(name, value)
                self.dump(req)
                resp = self.load()
                return resp.returnOrRaise()
            except KeyError:
                super().__setattr__(name, value)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return self.socket.__exit__(*args)

    return Proxy
