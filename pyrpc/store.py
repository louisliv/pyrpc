import inspect
from pyrpc.utils import (INVALID_REQUEST, 
    INVALID_PARAMS, METHOD_NOT_FOUND)
from pyrpc.serializers import (MethodSerializer,
    ErrorSerializer, ResultSerializer)
from rest_framework import status

def has_args(func):
    result = False
    args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(func)
    if args or varargs or varkw:
        result = True
    return result

def has_invalid_request(data):
    attributes_to_check = [
        { 'attribute': 'id' }, 
        { 'attribute': 'jsonrpc', 'value': ["2.0"] },
        { 'attribute': 'method' }
    ]

    for attribute_to_check in attributes_to_check:
        error_result = {
            'id': data.get('id', None),
            "jsonrpc": "2.0",
            "error": INVALID_REQUEST
        }
        attr = data.get(attribute_to_check['attribute'], None)
        if not attr:
            return error_result

        if (attribute_to_check.get('value', None) and
            attr not in attribute_to_check['value']):
            return error_result

    return
            

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

    def get_result(self, data):
        attribute_check = has_invalid_request(data)

        if attribute_check:
            return (ErrorSerializer(attribute_check).data,
                status.HTTP_400_BAD_REQUEST)

        method_name = data.get('method', None)

        obj_method = store.get_method(method_name)
        if not obj_method:
            data["error"] = METHOD_NOT_FOUND
            return (ErrorSerializer(data).data, 
                status.HTTP_400_BAD_REQUEST)

        if obj_method.has_args:
            params = data.get('params', None)

            if not params:
                data["error"] = INVALID_PARAMS
                return (ErrorSerializer(data).data,
                    status.HTTP_400_BAD_REQUEST)

            method_args = params.get('args', None)
            method_kwargs = params.get('kwargs', None)

            if not method_args and not method_kwargs:
                data["error"] = INVALID_PARAMS
                return (ErrorSerializer(data).data,
                    status.HTTP_400_BAD_REQUEST)

        try:
            if obj_method.has_args:
                if not method_kwargs:
                    data["result"] = obj_method(*method_args)
                    return (ResultSerializer(data).data,
                        status.HTTP_200_OK)
                elif not method_args:
                    data["result"] = obj_method(**method_kwargs)
                    return (ResultSerializer(data).data,
                        status.HTTP_200_OK)
                else:
                    data["result"] = obj_method(*method_args, **method_kwargs)
                    return (ResultSerializer(data).data,
                        status.HTTP_200_OK)
            else:
                data["result"] = obj_method()
                return (ResultSerializer(data).data,
                    status.HTTP_200_OK)
                
        except:
            data['error'] = INVALID_REQUEST
            return (ErrorSerializer(data).data,
                status.HTTP_400_BAD_REQUEST)

        

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