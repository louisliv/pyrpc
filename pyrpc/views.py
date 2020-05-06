from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from pyrpc.serializers import (MethodSerializer,
    ErrorSerializer, ResultSerializer)
from pyrpc.store import store
from pyrpc.utils import (INVALID_REQUEST, 
    INVALID_PARAMS, METHOD_NOT_FOUND)


class MethodViewSet(viewsets.ViewSet):
    def list(self, request):
        object_methods = store.get_all_methods()

        return Response(MethodSerializer(
            object_methods, many=True).data)

    def create(self, request):
        req_data = request.data
        result, status_code = store.get_result(req_data)
        return Response(result, status=status_code)

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
