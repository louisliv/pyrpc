from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from pyrpc.serializers import (MethodSerializer,
    ErrorSerializer, ResultSerializer)
from pyrpc.utils import (INVALID_REQUEST, 
    INVALID_PARAMS, METHOD_NOT_FOUND)

# Create your views here.
class MethodViewSet(viewsets.ViewSet):
    def list(self, request):
        obj = self.method_class()
        object_methods = [getattr(obj, method_name, None) 
            for method_name in dir(self.method_class)
            if getattr(getattr(obj, method_name), 'safe_method', None)]

        return Response(MethodSerializer(
            object_methods, many=True).data)

    def create(self, request):
        req_data = request.data

        jsonrpc = req_data.get('jsonrpc', None)
        
        if jsonrpc not in ["2.0"]:
            req_data["error"] = INVALID_REQUEST
            return Response(ErrorSerializer(req_data).data)
        
        obj = self.method_class()

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

        if not method_args or method_kwargs:
            req_data["error"] = INVALID_REQUEST
            return Response(ErrorSerializer(req_data).data)

        obj_method = getattr(obj, method_name, None)

        if obj_method and getattr(obj_method, 'safe_method', None):
            req_data["result"] = obj_method(*method_args, **method_kwargs)
            return Response(ResultSerializer(req_data).data)
        else:
            req_data["error"] = METHOD_NOT_FOUND
            return Response(ErrorSerializer(req_data).data)

    def retrieve(self, request, pk=None):
        obj = self.method_class()
        obj_method = getattr(obj, pk, None)
        return Response(MethodSerializer(obj_method).data)
