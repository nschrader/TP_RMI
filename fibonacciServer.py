from socket import socket
from pickle import dumps, loads

from fibonacci import Fibonacci

HOST = "localhost"
PORT = 1234

with socket() as soc:
    soc.bind((HOST, PORT))
    soc.listen()
    conn, addr = soc.accept()
    with conn:
        num = loads(conn.recv(4096))
        print(num)
        fib = Fibonacci()
        res = fib.calc(num)
        conn.sendall(dumps(res))
        print("ok")
