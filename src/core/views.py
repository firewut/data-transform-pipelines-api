from django.conf import settings
from rest_framework import viewsets


class ViewSetMetaClass(type):
    def __new__(cls, clsname, bases, dct):
        if settings.DEMO_MODE:
            return viewsets.ReadOnlyModelViewSet

        return viewsets.ModelViewSet


class BaseViewSet(object, metaclass=ViewSetMetaClass):
    pass
