from fibonacci import Fibonacci
from proxy import rmi

HOST = "localhost"
PORT = 1234

try:
    num = int(input("Enter a number: "))
    with rmi(Fibonacci, HOST, PORT)() as fib:
        res = fib.calc(num)
        print("F" + str(num) + " is " + str(res))
except ValueError:
    print("Not a number")
