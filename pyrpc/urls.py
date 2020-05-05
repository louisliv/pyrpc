from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from pyrpc.views import MethodViewSet

router = routers.DefaultRouter()
router.register(r'methods', MethodViewSet, basename="methods")

urls = [
    path('', include(router.urls)),
]