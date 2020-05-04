from rest_framework import serializers
import sys

def get_docstring_list(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return trimmed

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