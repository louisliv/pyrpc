class _MethodStore(object):
    def __init__(self):
        self.store = {}

    def add(self, func):
        func.safe = True
        self.store[func.__name__] = func

    def get_all_methods(self):
        return self.store.values()

    def get_method(self, name):
        return self.store.get(name, None)


store = _MethodStore()