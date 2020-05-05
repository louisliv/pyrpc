# coding: utf-8
import inspect
import warnings
from importlib import import_module

import django.core.checks
from django.apps import AppConfig
from pyrpc.store import store

from django.conf import settings

@django.core.checks.register()
def check_required_settings_defined(app_configs, **kwargs):
    result = []
    if not settings.METHOD_MODULES:
        result.append(
            django.core.checks.Warning(
                'settings.METHOD_MODULES is not set, pyrpc cannot locate your RPC methods.',
                hint='Add METHOD_MODULES in your settings.py.',
                obj=settings,
                id='pyrpc.E001',
            )
        )
    return result

class PyrpcConfig(AppConfig):
    name = 'pyrpc'

    def ready(self):
        self.init_store()

    @staticmethod
    def init_store():
        store.store.clear()

        if not settings.METHOD_MODULES:
            return

        for module_name in settings.METHOD_MODULES:

            try:
                method_module = import_module(module_name)

            except ImportError:
                msg = 'Cannot find "{}" declared in ' \
                    'settings.METHOD_MODULES.'.format(module_name)
                warnings.warn(msg, category=Warning)
                continue

            for _, func in inspect.getmembers(method_module, inspect.isfunction):
                if getattr(func, 'safe_method', None):
                    store.add(func)

            for _, mod_class in inspect.getmembers(method_module, inspect.isclass):
                for _, func in inspect.getmembers(mod_class, inspect.isfunction):
                    if getattr(func, 'safe_method', None):
                        store.add(func)