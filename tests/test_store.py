from pyrpc import store
from tests.utils import fixture
from django.test import TestCase

class AppTestCase(TestCase):

    def test_has_args(self):
        def no_args():
            pass

        result = store.has_args(no_args)

        assert(not result)

        def has_method_args(arg_1):
            pass

        result = store.has_args(has_method_args)

        assert(result)

        def has_method_varargs(*args):
            pass

        result = store.has_args(has_method_varargs)

        assert(result)

        def has_method_varkw(**kwargs):
            pass

        result = store.has_args(has_method_varkw)

        assert(result)

        def has_all_args(arg_1, *args, **kwargs):
            pass

        result = store.has_args(has_all_args)

        assert(result)

    def test_store_methods(self):
        mod_store = store.store
        test_fixture = fixture()
        internal_store = mod_store.get_store()
        internal_store.clear()

        mod_store.add(test_fixture['test_method'])

        assert(not getattr(test_fixture['test_method'], 'is_class_method'))

        assert(internal_store == {
            'plain_method': {
                "func": test_fixture['test_method']
            }
        })

        internal_store.clear()
        mod_func = getattr(test_fixture['test_class'], 'class_plain_method')
        mod_func_name = mod_func.__name__
        mod_store.add(
            mod_func, 
            class_method = True, 
            method_cls = test_fixture['test_class']
        )

        assert(getattr(mod_func, 'is_class_method'))

        assert(internal_store == {
            'class_plain_method': {
                "cls": test_fixture['test_class'],
                "func": mod_func
            }
        })

        internal_store.clear()

        mod_store.add(
            mod_func, 
            class_method = True, 
            method_cls = test_fixture['test_class']
        )
        mod_store.add(test_fixture['test_method'])

        assert(mod_store.get_all_methods() == [
            mod_func,
            test_fixture['test_method']
        ])
        retrieved_method = mod_store.get_method(mod_func_name).__func__

        assert(retrieved_method)

        retrieved_method = mod_store.get_method('plain_method')

        assert(retrieved_method)

        retrieved_method = mod_store.get_method('foobar')

        assert(not retrieved_method)

        internal_store.clear()
