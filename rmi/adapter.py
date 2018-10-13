def real(cls):
    class ContextManager(cls):
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

    return ContextManager
