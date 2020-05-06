from pyrpc import utils
from django.test import TestCase

class AppTestCase(TestCase):
    def test_get_docstring_list(self):
        def placeholder_method():
            """ 
            test

            @param test: test
            @returns: pass
            """
            pass

        def no_docstring():
            pass

        docstring_list = utils.get_docstring_list(
            placeholder_method.__doc__)

        assert(docstring_list == [
            'test', 
            '', 
            '@param test: test', 
            '@returns: pass']
        )

        docstring_list = utils.get_docstring_list(
            no_docstring.__doc__)

        assert(docstring_list == '')
