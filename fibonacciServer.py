from socketserver import StreamRequestHandler, TCPServer
from pickle import dump, load
from importlib import import_module

HOST = "localhost"
PORT = 1234
ACK = b"ack\n"

class RmiHandler(StreamRequestHandler):
    def handle(self):
        try:
            cModule, cName, cArgs, cKwargs = load(self.rfile)
            cls = getattr(import_module(cModule), cName)
            inst = cls(*cArgs, **cKwargs)
            self.wfile.write(ACK)

            pName, pArgs, pKwargs = load(self.rfile)
            func = getattr(inst, pName)
            res = func(*pArgs, **pKwargs)
            dump(res, self.wfile)
        except EOFError:
            pass

class Server(TCPServer):
    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)

try:
    server = Server((HOST, PORT), RmiHandler)
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    print("closing")
    server.server_close()
