from fibonacciRMI import Fibonacci

try:
    num = int(input("Enter a number: "))
    fib = Fibonacci()
    res = fib.calc(num)
    print("F" + str(num) + " is " + str(res))
except ValueError:
    print("Not a number")
