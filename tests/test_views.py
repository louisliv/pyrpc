# from pyrpc.store import store
from django.urls import reverse
from rest_framework.test import APITestCase
from django.apps import apps as django_apps
import json
from tests.utils import METHODS_LIST, not_found
from pyrpc.serializers import (MethodSerializer,
    ErrorSerializer)
from pyrpc.utils import (METHOD_NOT_FOUND,
    INVALID_REQUEST, INVALID_PARAMS)

def compare_lists(a, b):
    return sorted(a) == sorted(b)

class MethodViewSetTests(APITestCase):
    def test_list(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            serializer = MethodSerializer(
                METHODS_LIST, many=True).data
            
            url = reverse('methods-list')
            response = self.client.get(
                url, {}, format='json')

            data = json.dumps(response.data)
            serial = json.dumps(serializer)

            assert(compare_lists(data, serial))

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_retrieve(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            first_method = METHODS_LIST[0]

            serializer = MethodSerializer(first_method).data
            
            url = reverse('methods-detail', 
                args=[first_method.__name__])
            response = self.client.get(
                url, {}, format='json')

            data = json.dumps(response.data)
            serial = json.dumps(serializer)

            assert(data == serial)

            serializer = ErrorSerializer({
                "id": 1,
                "jsonrpc": "2.0",
                "error": METHOD_NOT_FOUND
            })

            url = reverse('methods-detail', 
                args=[not_found.__name__])
            response = self.client.get(
                url, {}, format='json')

            data = json.dumps(response.data)
            serial = json.dumps(serializer.data)

            assert(data == serial)

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_errors(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            post_data = {
                "jsonrpc": "2.0",
                "method": 'has_method_args'
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(data['id'], None)
            self.assertEquals(
                data['error']['code'], 
                INVALID_REQUEST['code']
            )

            post_data = {
                "id": 1,
                "jsonrpc": "1.0",
                "method": 'has_method_args'
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(
                data['error']['code'], 
                INVALID_REQUEST['code']
            )

            post_data = {
                "id": 1,
                "jsonrpc": "2.0"
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(
                data['error']['code'], 
                INVALID_REQUEST['code']
            )

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_method_not_found(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            post_data = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "test"
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(
                data["error"]["code"],
                METHOD_NOT_FOUND['code']    
            )

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_no_params(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            post_data = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "has_method_args"
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(
                data["error"]["code"],
                INVALID_PARAMS['code']    
            )

            post_data["params"] = {"test":1}

            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(
                data["error"]["code"],
                INVALID_PARAMS['code']    
            )

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_one_kwarg(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            post_data = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "has_method_args",
                "params": {
                    "kwargs":{"arg_1":1}
                }
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(data["result"], 4)

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_with_args(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            post_data = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "has_method_varargs",
                "params": {
                    "args": [1]
                }
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(data["result"], 5)

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_with_all_args(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            post_data = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "has_all_args",
                "params": {
                    "args": [1],
                    "kwargs": {"arg_2": 1}
                }
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(data["result"], 7)

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_with_no_args(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            post_data = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "plain_method"
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(data["result"], 3)

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()

    def test_with_error(self):
        with self.settings(
            METHOD_MODULES=['tests.utils']):
            app_config = django_apps.get_app_config('pyrpc')
            app_config.ready()

            post_data = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "has_method_args",
                "params": {
                    "kwargs": { "test": 1 }
                }
            }
            
            url = reverse('methods-list')
            response = self.client.post(
                url, post_data, format='json')

            data = response.data

            self.assertEquals(
                data["error"]["code"],
                INVALID_REQUEST['code']    
            )

        app_config = django_apps.get_app_config('pyrpc')
        app_config.ready()