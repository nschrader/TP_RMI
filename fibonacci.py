class Fibonacci:
    def __init__(self):
        self.index = 0

    def next(self):
        self.index += 1
        return self.calc(self.index)

    def string(self):
        return "F" + str(self.index) + " is " + str(self.calc(self.index))

    def calc(self, a):
        if a is 0 or a is 1:
            return a
        else:
            return self.calc(a-1) + self.calc(a-2);
