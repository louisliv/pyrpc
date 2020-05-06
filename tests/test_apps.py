from pyrpc import apps
from pyrpc.store import store
from pyrpc.decorators import safe_method
from django.test import TestCase
from django.apps import apps as django_apps
from tests.utils import PlainClass

class AppTestCase(TestCase):
    def test_check_settings(self):
        fixture = ['Test']

        with self.settings(METHOD_MODULES=fixture):
            result = apps.check_settings({}, **{})

            assert(not result)

        fixture = []

        with self.settings(METHOD_MODULES=fixture):
            result = apps.check_settings({}, **{})

            assert(result)

    def test_config(self):
        fixture = []
        app_config = django_apps.get_app_config('pyrpc')

        mod_store = store.get_store()
        mod_store.clear()
        with self.settings(METHOD_MODULES=fixture):
            assert(not app_config.init_store())

        fixture = ['Test']
        mod_store.clear()
        with self.settings(METHOD_MODULES=fixture):
            assert(not app_config.init_store())

        fixture = ['tests.utils']
        mod_store.clear()

        with self.settings(METHOD_MODULES=fixture):
            safe_method(PlainClass.class_plain_method)
            assert(not app_config.init_store())
            delattr(PlainClass.class_plain_method, 'safe_method')
        mod_store.clear()
