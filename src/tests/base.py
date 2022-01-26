import json
import importlib
import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIRequestFactory
import celery
import mock
import requests

from core.utils import *
from core.utils.url import urljoin
from projects.views import ProjectsViewSet


class TestMetaClass(type):
    def __new__(mcs, name, bases, dct):
        for attr_name in list(dct.keys()):
            if hasattr(dct[attr_name], "test_cases"):
                cases = dct[attr_name].test_cases
                del dct[attr_name].test_cases
                hidden_name = "__" + attr_name
                mcs._move_method(dct, attr_name, hidden_name)

                for case in cases:
                    mcs._add_test_method(dct, attr_name, hidden_name, case[0], case[1:])

        return super(TestMetaClass, mcs).__new__(mcs, name, bases, dct)

    @classmethod
    def _move_method(mcs, dct, from_name, to_name):
        dct[to_name] = dct[from_name]
        dct[to_name].__name__ = str(to_name)
        del dct[from_name]

    @classmethod
    def _add_test_method(mcs, dct, orig_name, hidden_name, postfix, params):
        test_method_name = "{}__{}".format(orig_name, postfix)

        def test_method(self):
            return getattr(self, hidden_name)(*params)

        test_method.__name__ = str(test_method_name)
        dct[test_method_name] = test_method


class BaseTestCase(TestCase, metaclass=TestMetaClass):
    viewset = None
    user = None
    page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]

    images_dir = os.path.join(os.path.dirname(__file__), "data")
    image_path = os.path.join(images_dir, "image.png")

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

    def urljoin(self, *args):
        return urljoin(*args)

    def setUp(self):
        super().setUp()

        # Sync processors
        call_command("sync_processors")

        def send_task_apply(*args, **kwargs):
            task_name = args[0].split(".")[-1]
            module = importlib.import_module(".".join(args[0].split(".")[:-1]))

            task = getattr(module, task_name).s(**kwargs["kwargs"]).apply()

            if task.status == "FAILURE":
                raise Exception("{}.{} {}".format(module, task_name, task.result))

        mock.patch.object(
            celery.current_app,
            "send_task",
            side_effect=send_task_apply,
            return_value=True,
        ).start()

    def random_image(self, width=500, height=500):
        return random_image(width, height)

    def random_string(self, N=10):
        return random_string(N)

    def random_uuid(self):
        return random_uuid4()

    def random_url(self):
        return "http://{}.{}/{}".format(
            self.random_string(7), self.random_string(3), self.random_string(5)
        )

    def put_create(
        self, data, user=None, action="create", viewset=None, _format="json"
    ):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        created = viewset.as_view(actions={"put": action})

        request = factory.put("", data=data, format=_format)
        response = created(request)
        response.render()

        as_dict = None
        try:
            as_dict = json.loads(response.content)
        except Exception as e:
            pass
        return response, as_dict

    def put_update(
        self, pk: str, data, action="update", user=None, viewset=None, _format="json"
    ):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        updated = viewset.as_view(
            actions={
                "put": action,
            }
        )

        request = factory.put("", data=data, format=_format)
        response = updated(request, pk=pk)
        response.render()

        as_dict = None
        try:
            as_dict = json.loads(response.content)
        except Exception as e:
            pass
        return response, as_dict

    def post_create(
        self, data, pk=None, user=None, action="create", viewset=None, _format="json"
    ):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        created = viewset.as_view(actions={"post": action})

        request = factory.post("", data=data, format=_format)
        response = created(request, pk=pk)
        response.render()

        as_dict = None
        try:
            as_dict = json.loads(response.content)
        except Exception as e:
            pass
        return response, as_dict

    def get_item(self, pk: str, data=None, user=None, action="retrieve", viewset=None):
        if not viewset:
            viewset = self.viewset

        factory = APIRequestFactory()
        retrieved = viewset.as_view(actions={"get": action})

        request = factory.get("", data=data)
        response = retrieved(request, pk=pk)
        response.render()

        as_dict = None
        try:
            as_dict = json.loads(response.content)
        except Exception as e:
            pass
        return response, as_dict

    def get_list(self, user=None, viewset=None):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        listed = viewset.as_view(actions={"get": "list"})

        request = factory.get("")
        response = listed(request)
        response.render()

        as_dict = None
        try:
            as_dict = json.loads(response.content)
        except Exception as e:
            pass
        return response, as_dict

    def create_project(self, user=None, **kwargs):
        if not user:
            user = self.user

        data = {"title": self.random_string(), "description": self.random_string(50)}
        data.update(kwargs)
        return self.post_create(data, user=user, viewset=ProjectsViewSet)

    def patch_update(
        self, pk: str, data: dict, user=None, viewset=None, _format="json"
    ):
        if viewset is None:
            viewset = self.viewset

        factory = APIRequestFactory()
        patched = viewset.as_view(
            actions={
                "patch": "partial_update",
            }
        )

        request = factory.patch("", data=data, format=_format)

        response = patched(request, pk=pk)
        response.render()

        as_dict = None
        try:
            as_dict = json.loads(response.content)
        except Exception as e:
            pass
        return response, as_dict

    def _fake_http_response(
        self,
        status=200,
        content=None,
        json_data=None,
        cookies=None,
        headers=None,
    ):
        response = requests.Response()
        response.code = "Ok"
        if headers:
            response.headers = headers
        response.status_code = status
        response._content = str.encode(json.dumps(json_data))
        response.cookies = cookies or {"CookieKey": "CookieValue"}

        return response
