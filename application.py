from fibonacci import Fibonacci
from rmi import stub

HOST = "localhost"
PORT = 1234

try:
    num = int(input("Enter a number: "))
    with stub(Fibonacci, HOST, PORT)() as fib:
        res = fib.calc(num)
        print("F" + str(num) + " is " + str(res))
except ValueError:
    print("Not a number")
