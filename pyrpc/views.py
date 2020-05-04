from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from pyrpc.serializers import MethodSerializer

# Create your views here.
class MethodViewSet(viewsets.ViewSet):
    def list(self, request):
        obj = self.method_class()
        object_methods = [getattr(obj, method_name, None) for method_name in dir(self.method_class)
            if getattr(getattr(obj, method_name), 'safe_method', None)]

        return Response(MethodSerializer(object_methods, many=True).data)

    def create(self, request):
        obj = self.method_class()
        req_data = request.data

        method_name = req_data.get('method', None)
        
        if not method_name:
            return Response("Function not provided", 
                status=status.HTTP_400_BAD_REQUEST)

        method_args = req_data.get('args', None)
        method_kwargs = req_data.get('kwargs', None)

        obj_method = getattr(obj, method_name, None)

        if obj_method and getattr(obj_method, 'safe_method', None):
            return Response(obj_method(*method_args, **method_kwargs))
        elif not obj_method:
            return Response("Function not found.", 
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Function not allowed.", 
                status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = self.method_class()
        obj_method = getattr(obj, pk, None)
        return Response(MethodSerializer(obj_method).data)

    def update(self, request, pk=None):
        obj = self.method_class()

        req_data = request.data

        method_args = req_data.get('args', None)
        method_kwargs = req_data.get('kwargs', None)

        obj_method = getattr(obj, pk, None)

        if obj_method and getattr(obj_method, 'safe_method', None):
            return Response(obj_method(*method_args, **method_kwargs))
        elif not obj_method:
            return Response("Function not found.", 
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Function not allowed.", 
                status=status.HTTP_400_BAD_REQUEST)
