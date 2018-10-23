import random
import string
import uuid

from django.conf import settings
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from projects.views import (
    ProjectsViewSet
)

class TestMetaClass(type):
    def __new__(mcs, name, bases, dct):
        for attr_name in list(dct.keys()):
            if hasattr(dct[attr_name], 'test_cases'):
                cases = dct[attr_name].test_cases
                del dct[attr_name].test_cases
                hidden_name = '__' + attr_name
                mcs._move_method(dct, attr_name, hidden_name)

                for case in cases:
                    mcs._add_test_method(
                        dct, attr_name, hidden_name, case[0], case[1:])

        return super(TestMetaClass, mcs).__new__(mcs, name, bases, dct)

    @classmethod
    def _move_method(mcs, dct, from_name, to_name):
        dct[to_name] = dct[from_name]
        dct[to_name].__name__ = str(to_name)
        del dct[from_name]

    @classmethod
    def _add_test_method(mcs, dct, orig_name, hidden_name, postfix, params):
        test_method_name = '{}__{}'.format(orig_name, postfix)

        def test_method(self):
            return getattr(self, hidden_name)(*params)
        test_method.__name__ = str(test_method_name)
        dct[test_method_name] = test_method


class BaseTestCase(TestCase, metaclass=TestMetaClass):
    viewset = None
    user = None
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

    @classmethod
    def cases(cls, *cases):
        """
        Create a bunch of test methods using the case table and test code.

        Example. The following two pieces of code would behave identically:

        @BaseTestCase.cases(['name1', 1], ['name2', 2])
        def test_example(self, number):
            self.assertGreater(number, 0)

        def __test_example(self, number):
            self.assertGreater(number, 0)
        def test_example__name1(self):
            return self.__test_example(1)
        def test_example__name2(self):
            return self.__test_example(2)
        """

        def decorator(test_method):
            test_method.test_cases = cases
            return test_method

        return decorator

    def setUp(self):
        super().setUp()

    def random_string(self, N=10):
        return ''.join(
            random.choice(
                string.ascii_letters + string.digits
            ) for x in range(N)
        )

    def random_uuid(self):
        return str(uuid.uuid4())

    def put_create(self, data: dict, user=None, viewset=None):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        created = viewset.as_view(actions={'put': 'create'})

        request = factory.put("", data=data, format='json')
        return created(request)

    def put_update(self, pk: str, data: dict, user=None, viewset=None):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        created = viewset.as_view(
            actions={
                'put': 'update',
            }
        )

        request = factory.put("", data=data, format='json')
        return created(request, pk=pk)

    def post_create(self, data: dict, user=None, viewset=None):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        created = viewset.as_view(actions={'post': 'create'})

        request = factory.post("", data=data, format='json')
        return created(request)

    def get_list(self, user=None, viewset=None):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        listed = viewset.as_view(actions={'get': 'list'})

        request = factory.get("")
        return listed(request)

    def create_project(self, user=None, **kwargs):
        if not user:
            user = self.user

        data = {
            'title': self.random_string(),
            'description': self.random_string(50)
        }
        data.update(kwargs)
        return self.post_create(
            data,
            user=user,
            viewset=ProjectsViewSet
        )

    def patch_update(self, pk: str, data: dict, user=None, viewset=None):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        created = viewset.as_view(
            actions={
                'patch': 'partial_update',
            }
        )

        request = factory.patch("", data=data, format='json')
        return created(request, pk=pk)
