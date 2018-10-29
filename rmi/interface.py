class ClassRequest:
    def __init__(self, mName, cName, args, kwargs):
        self.mName = mName
        self.cName = cName
        self.args = args
        self.kwargs = kwargs

class GetAttributeRequest:
    def __init__(self, name):
        self.name = name

class SetAttributeRequest:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class MethodRequest:
    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

class Response:
    def __init__(self, raisedException, returnOrException=None):
        self.raisedException = raisedException
        self.returnOrException = returnOrException

    def returnOrRaise(self):
        if self.raisedException:
            print(self.returnOrException)
            raise self.returnOrException
        else:
            return self.returnOrException

class RequestOutOfOrderException(Exception):
    def __init__(self, request, *requestClasses):
        fmt = "Request out of order. Expected one of the follwing {} but got {}"
        super().__init__(fmt.format(requestClasses, request))
