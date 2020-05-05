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

INVALID_REQUEST = { "code": -32600, "message": "Invalid Request" }
PARSE_ERROR = { "code": -32700, "message": "Parse error" }
INVALID_REQUEST = { "code": -32600, "message": "Invalid Request" }
METHOD_NOT_FOUND = { "code": -32601, "message": "Method not found" }
INVALID_PARAMS = { "code": -32602, "message": "Invalid params" }
SERVER_ERROR = { "code": -32000, "message": "Server error" }
