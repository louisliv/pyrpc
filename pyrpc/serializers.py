from rest_framework import serializers
from pyrpc.utils import get_docstring_list

def is_description_line(line):
    return (line not in [''] 
        and not line.startswith('@param')
        and not line.startswith('@return'))

def is_param_line(line):
    return line.startswith('@param')

def is_return_line(line):
    return line.startswith('@returns')


class MethodSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    kwargs = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    returns = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.__name__

    def get_kwargs(self, obj):
        docstring_list = get_docstring_list(obj.__doc__)
        params = {}

        for line in docstring_list:
            if is_param_line(line):
                param_name = line.split('@param ')[1].split(': ')[0]
                param_desc = line.split('@param ')[1].split(': ')[1]

                params[param_name] = param_desc
        return params

    def get_returns(self, obj):
        docstring_list = get_docstring_list(obj.__doc__)
        return_line = ''

        for line in docstring_list:
            if is_return_line(line):
                return_line = line.split('@returns: ')[1]
        return return_line

    def get_description(self, obj):
        docstring_list = get_docstring_list(obj.__doc__)
        trimmed_docstring_list = [line for line in docstring_list
            if is_description_line(line)]
        return trimmed_docstring_list


class ErrorSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    jsonrpc = serializers.SerializerMethodField()
    error = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj['id']

    def get_jsonrpc(self, obj):
        return "2.0"

    def get_error(self, obj):
        return obj['error']

class ResultSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    jsonrpc = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj['id']

    def get_jsonrpc(self, obj):
        return "2.0"

    def get_result(self, obj):
        return obj['result']
