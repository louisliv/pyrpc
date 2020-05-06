import inspect

def has_args(func):
    result = False
    args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(func)
    if args or varargs or varkw:
        result = True
    return result


class _MethodStore(object):
    def __init__(self):
        self.store = {}

    def add(self, func, class_method = False, method_cls = None):
        func.has_args = has_args(func)
        func.is_class_method = class_method

        if not class_method:
            self.store[func.__name__] = { "func": func }
        else:
            self.store[func.__name__] = {
                "cls": method_cls,
                "func": func
            }

    def get_store(self):
        return self.store

    def get_all_methods(self):
        values = []
        store_values = self.store.values()

        for store_value in store_values:
            values.append(store_value['func'])
        return values

    def get_method(self, name):
        store_obj = self.store.get(name, None)
        if store_obj:
            method_cls = store_obj.get('cls', None) 
            if method_cls:
                obj = method_cls()
                store_method = getattr(obj, name)
            else:
                store_method = store_obj.get('func')
            return store_method 
        return None


store = _MethodStore()