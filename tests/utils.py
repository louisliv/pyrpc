from pyrpc.decorators import safe_method

def plain_method():
    return 1+2

def has_method_args(arg_1):
    return 1+3

def has_method_varargs(*args):
    return 1+4

def has_method_varkw(**kwargs):
    return 1+5

def has_all_args(arg_1, *args, **kwargs):
    return 1+6

def not_found():
    pass

class PlainClass():
    def class_plain_method(self):
        pass

METHODS_LIST = [
    has_method_args, 
    has_method_varargs,
    has_method_varkw,
    has_all_args,
    plain_method
]
METHODS = {}

for method in METHODS_LIST:
    safe_method(method)
    METHODS[method.__name__] = method

def fixture():
    fixture = {}

    fixture['test_class'] = PlainClass
    fixture['test_method'] = plain_method

    return fixture