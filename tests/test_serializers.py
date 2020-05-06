from pyrpc import serializers
import json
from django.test import TestCase

class AppTestCase(TestCase):
    def test_is_description_line(self):
        line = 'Test'

        assert(serializers.is_description_line(line))
        
        line = '@param'

        assert(not serializers.is_description_line(line))

        line = '@return'

        assert(not serializers.is_description_line(line))

        line = ''

        assert(not serializers.is_description_line(line))

    def test_is_param_line(self):
        line = 'Test'

        assert(not serializers.is_param_line(line))
        
        line = '@param'

        assert(serializers.is_param_line(line))

    def test_is_return_line(self):
        line = 'Test'

        assert(not serializers.is_return_line(line))
        
        line = '@returns'

        assert(serializers.is_return_line(line))

    def test_method_serializer(self):
        def placeholder_method():
            """ 
            test

            @param test: test
            @returns: pass
            """
            pass

        should_return = {
            "name": "placeholder_method",
            "kwargs": {
                "test": "test"
            },
            "description": [
                "test"
            ],
            "returns": "pass"
        }

        serializer = serializers.MethodSerializer(placeholder_method).data

        assert(serializer == should_return)

    def test_error_serializer(self):
        fixture = {
            "id": 1,
            "error": "test" 
        }

        should_return = {
            "id": 1,
            "jsonrpc": "2.0",
            "error": "test"
        }

        serializer = serializers.ErrorSerializer(fixture).data

        assert(serializer == should_return)

    def test_result_serializer(self):
        fixture = {
            "id": 1,
            "result": "test" 
        }

        should_return = {
            "id": 1,
            "jsonrpc": "2.0",
            "result": "test"
        }

        serializer = serializers.ResultSerializer(fixture).data

        assert(serializer == should_return)
