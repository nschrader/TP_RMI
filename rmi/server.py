from socketserver import StreamRequestHandler, ForkingTCPServer
from importlib import import_module

from .interface import *
from .misc import PickleMixin

HOST = "localhost"
PORT = 1234
SECS = 1
TIMEOUT = 5*SECS

class RmiHandler(StreamRequestHandler, PickleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request.settimeout(TIMEOUT)

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

            # Access instance
            while (True):
                try:
                    req = self.load()
                    # Invoke method
                    if isinstance(req, MethodRequest):
                        func = getattr(inst, req.name)
                        res = func(*req.args, **req.kwargs)
                        resp = Response(raisedException=False, returnOrException=res)
                    # Get attribute
                    elif isinstance(req, GetAttributeRequest):
                        attr = getattr(inst, req.name)
                        resp = Response(raisedException=False, returnOrException=attr)
                    # Set attribute
                    elif isinstance(req, SetAttributeRequest):
                        setattr(inst, req.name, req.value)
                        resp = Response(raisedException=False)
                    else:
                        raise RequestOutOfOrderException(req, MethodRequest, GetAttributeRequest, SetAttributeRequest)
                except Exception as e:
                    resp = Response(raisedException=True, returnOrException=e)
                finally:
                    self.dump(resp)

        except EOFError:
            pass

class Server(ForkingTCPServer):
    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)

    def handle_error(request, client_address):
        pass

def skeleton():
    try:
        server = Server((HOST, PORT), RmiHandler)
        server.serve_forever()
    finally:
        server.server_close()
