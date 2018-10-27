from socketserver import StreamRequestHandler, TCPServer
from importlib import import_module

from .interface import *
from .misc import PickleMixin

HOST = "localhost"
PORT = 1234

class RmiHandler(StreamRequestHandler, PickleMixin):
    def handle(self):
        try:
            # Instanciate class
            try:
                req = self.load()
                if not isinstance(req, ClassRequest):
                    raise RequestOutOfOrderException(req, ClassRequest)
                cls = getattr(import_module(req.mName), req.cName)
                inst = cls(*req.args, **req.kwargs)
                resp = Response(raisedException=False)
            except Exception as e:
                resp = Response(raisedException=True, returnOrException=e)
            finally:
                self.dump(resp)

            # Invoke mathods
            while (True):
                try:
                    req = self.load()
                    if isinstance(req, MethodRequest):
                        func = getattr(inst, req.name)
                        res = func(*req.args, **req.kwargs)
                        resp = Response(raisedException=False, returnOrException=res)
                    elif isinstance(req, AttributeRequest):
                        attr = getattr(inst, req.name)
                        resp = Response(raisedException=False, returnOrException=attr)
                    else:
                        raise RequestOutOfOrderException(req, MethodRequest, AttributeRequest)
                except Exception as e:
                    resp = Response(raisedException=True, returnOrException=e)
                finally:
                    self.dump(resp)

        except EOFError:
            pass

class Server(TCPServer):
    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)

def skeleton():
    try:
        server = Server((HOST, PORT), RmiHandler)
        server.serve_forever()
    finally:
        server.server_close()
