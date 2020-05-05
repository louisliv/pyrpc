from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from pyrpc.serializers import (MethodSerializer,
    ErrorSerializer, ResultSerializer)
from pyrpc.store import store
from pyrpc.utils import (INVALID_REQUEST, 
    INVALID_PARAMS, METHOD_NOT_FOUND)

# Create your views here.
class MethodViewSet(viewsets.ViewSet):
    def list(self, request):
        object_methods = store.get_all_methods()

        return Response(MethodSerializer(
            object_methods, many=True).data)

    def create(self, request):
        req_data = request.data
        
        if not req_data.get('id', None):
            req_error = {
                "id": '',
                "jsonrpc": "2.0",
                "error": INVALID_REQUEST
            }
            return Response(ErrorSerializer(req_error).data)

        jsonrpc = req_data.get('jsonrpc', None)
        
        if jsonrpc not in ["2.0"]:
            req_data["error"] = INVALID_REQUEST
            return Response(ErrorSerializer(req_data).data)

        method_name = req_data.get('method', None)
            
        if not method_name:
            req_data["error"] = INVALID_REQUEST
            return Response(ErrorSerializer(req_data).data)

        params = req_data.get('params', None)

        if not params:
            req_data["error"] = INVALID_PARAMS
            return Response(ErrorSerializer(req_data).data)

        method_args = params.get('args', None)
        method_kwargs = params.get('kwargs', None)

        if not method_args and not method_kwargs:
            req_data["error"] = INVALID_PARAMS
            return Response(ErrorSerializer(req_data).data)

        try:
            obj_method = store.get_method(method_name)

            if obj_method:
                req_data["result"] = obj_method(*method_args, **method_kwargs)
                return Response(ResultSerializer(req_data).data)
            else:
                req_data["error"] = METHOD_NOT_FOUND
                return Response(ErrorSerializer(req_data).data)
        except:
            req_data['error']: INVALID_REQUEST
            return Response(ResultSerializer(req_data).data)

    def retrieve(self, request, pk=None):
        obj_method = store.get_method(pk)

        if obj_method:
            return Response(MethodSerializer(obj_method).data)
        else:
            req_data = {
                "id": 1
            }
            req_data["error"] = METHOD_NOT_FOUND
            return Response(ErrorSerializer(req_data).data)
