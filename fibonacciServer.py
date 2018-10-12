from socket import socket, SOL_SOCKET, SO_REUSEADDR
from pickle import dumps, loads

from fibonacci import Fibonacci

HOST = "localhost"
PORT = 1234
ACK = b"ack"

with socket() as sock:
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind((HOST, PORT))
    sock.listen(10)
    conn, addr = sock.accept()
    with conn:
        args, kwargs = loads(conn.recv(4096))
        conn.send(ACK)
        fib = Fibonacci(*args, **kwargs)

        print(args)
        print(kwargs)
        params = loads(conn.recv(4096))
        print(params)
        num = 10
        res = fib.calc(num)
        conn.sendall(dumps(res))
