from pyrpc.decorators import safe_method
from django.test import TestCase

class AppTestCase(TestCase):
    def test_safe_method(self):

        @safe_method
        def empty():
            pass

        def really_empty():
            pass

        assert getattr(empty, 'safe_method')
        assert not getattr(really_empty, 'safe_method', None)
