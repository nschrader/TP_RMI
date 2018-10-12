class Fibonacci:

    def calc(self, a):
        if a is 0 or a is 1:
            return a
        else:
            return self.calc(a-1) + self.calc(a-2);
