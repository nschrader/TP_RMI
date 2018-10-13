from fibonacci import Fibonacci
from rmi import stub

HOST = "localhost"
PORT = 1234

with stub(Fibonacci, HOST, PORT)() as fib:
    try:
        num = int(input("Enter a number: "))
        res = fib.calc(num)
        print("Statically caclulated F" + str(num) + " is " + str(res) + "\n")

        print("Press ENTER to generate the next Fibonacci Number", end="")
        while (True):
            input()
            fib.next()
            print(fib.string(), end="")

    except ValueError:
        print("Not a number")
    except KeyboardInterrupt:
        print()
        pass
