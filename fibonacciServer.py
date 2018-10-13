from socketserver import StreamRequestHandler, TCPServer
from pickle import dump, load

from fibonacci import Fibonacci

HOST = "localhost"
PORT = 1234
ACK = b"ack\n"

class RmiHandler(StreamRequestHandler):
    def handle(self):
        try:
            cArgs, cKwargs = load(self.rfile)
            fib = Fibonacci(*cArgs, **cKwargs) #TODO: Use real class
            self.wfile.write(ACK)

            pArgs, pKwargs = load(self.rfile)
            res = fib.calc(*pArgs, **pKwargs) #TODO: Use real function
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
