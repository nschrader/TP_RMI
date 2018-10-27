from pickle import dump as pickle_dump, load as pickle_load

def real(cls):
    class ContextManager(cls):
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

    return ContextManager

class PickleMixin:
    def dump(self, obj):
        try:
            pickle_dump(obj, self.wfile)
        except BrokenPipeError:
            pass

    def load(self):
        try:
            return pickle_load(self.rfile)
        except BrokenPipeError:
            pass
