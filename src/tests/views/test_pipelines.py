import copy
import io
import json
import os

from django.db.transaction import TransactionManagementError
from django.conf import settings
import mock

from projects.views import *
from projects.models import *
from tests.base import BaseTestCase


class PipelinesBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        project_response, response_json = self.create_project({
            'title': self.random_string(30),
            'description': self.random_string(100),
        })
        self.assertEqual(project_response.status_code, 201)
        self.project_id = response_json['id']

        self.project = Project.objects.get(pk=self.project_id)

    def tearDown(self):
        try:
            self.project.delete()
            self.assertIsNone(self.project.pk)

            if hasattr(self, 'pipeline'):
                self.pipeline.delete()
                self.assertIsNone(self.pipeline.pk)

                if hasattr(self, 'pipeline_result'):
                    self.pipeline_result.delete()
                    self.assertIsNone(self.pipeline_result.pk)
        except TransactionManagementError as e:
            pass

        super().tearDown()


class PipelinesTestCase(PipelinesBaseTestCase):
    viewset = PipelineViewSet

    @BaseTestCase.cases(
        ('empty_processors', [], 201),
        ('null_processors', None, 201),
        ('existing_processors', [{'id': 'md5'}], 201),
        ('missing_processors', [{'id': 'md666'}], 400),
    )
    def test_create_pipeline(self, processors: [], status_code: int):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": processors
        }

        response, response_json = self.post_create(pipeline_data)
        self.assertEqual(response.status_code, status_code, response_json)
        if status_code == 400:
            self.assertEqual(
                response_json,
                {
                    "processors": [
                        "Processors does not exist: ['md666']"
                    ]
                }
            )

    def test_update_pipeline_via_post_twice(self):
        pipeline_id = self.random_uuid()
        pipeline_data = {
            "id": pipeline_id,
            "title": self.random_string(),
            "project": self.project_id,
            "processors": []
        }

        response, response_json = self.post_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response_json)

        response, response_json = self.post_create(pipeline_data)
        self.assertEqual(response.status_code, 409, response_json)

    def test_update_via_put(self):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": []
        }

        response, response_json = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response_json)
        # data.get('id', data.get('pk'))
        response, response_json = self.put_update(
            pipeline_data.get('id'),
            pipeline_data
        )
        self.assertEqual(response.status_code, 200, response_json)

    def test_update_via_patch(self):
        pipeline_id = self.random_uuid()
        pipeline_data = {
            "id": pipeline_id,
            "title": self.random_string(),
            "project": self.project_id,
            "processors": []
        }

        response, response_json = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response_json)

        processors = [{'id': 'md5'}]
        _pipeline_data = copy.deepcopy(pipeline_data)
        _pipeline_data.update({
            'processors': processors
        })
        response, response_json = self.patch_update(
            _pipeline_data.get('id'),
            _pipeline_data
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertEqual(response_json['processors'][0]['id'], 'md5')

    def test_processors_correct_order(self):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": "readability"
                },
                {
                    "id": "get_object_property",
                    "in_config": {
                        "property": "content"
                    }
                },
                {
                    "id": "google_translate",
                    "in_config": {
                        "from": "en",
                        "to": "ru",
                        "api_key": "<YOUR_API_KEY>"
                    }
                }
            ]
        }

        response, response_json = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response_json)

    def test_processors_incorrect_order(self):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": "readability"
                },
                {
                    "id": "google_translate",
                    "in_config": {
                        "from": "en",
                        "to": "ru",
                        "api_key": "<YOUR_API_KEY>"
                    }
                }
            ]
        }

        response, response_json = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 400, response_json)
        self.assertIn(
            "readability[0] is incompatible with next processor google_translate",
            str(response_json),
        )

    def test_processors_incorrect_in_config(self):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": "random",
                    "in_config": {
                        "length": 101,
                        "random_type": "string"
                    }
                }
            ]
        }

        response, response_json = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 400, response_json)
        self.assertIn(
            "random[0] has invalid in_config",
            str(response_json),
            response_json
        )

    @BaseTestCase.cases(
        (
            'random_none',
            'random',
            {"length": 10, "random_type": "string"},
            {'data': None},
        ),
        (
            'random_empty',
            'random',
            {"length": 10, "random_type": "string"},
            {'data': {}},
        ),
        (
            'get_object_property_empty',
            'get_object_property',
            {"property": "lala"},
            {'data': {}},
        ),
        (
            'get_object_property',
            'get_object_property',
            {"property": "lala"},
            {'data': {"lala": "123"}},
        ),
        (
            'html_to_text_empty',
            'html_to_text',
            {},
            {'data': ""},
        ),
    )
    def test_processors_valid_input_data(
        self,
        processor_id,
        in_config,
        in_data
    ):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": processor_id,
                    "in_config": in_config
                }
            ]
        }
        response, response_json = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response_json)

        response, response_json = self.put_update(
            pipeline_data.get('id'),
            in_data,
            action='process'
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(
            response_json['pipeline'],
            pipeline_data['id'],
        )
        self.assertIn(
            'pipeline_result/{}/'.format(
                response_json.get('id')
            ),
            response['Location'],
        )

    def test_resize_and_grayscale(self):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": "resize_image",
                    "in_config": {
                        "size": [100, 100]
                    }
                },
                {
                    "id": "grayscale_image"
                }
            ]
        }
        response, response_json = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response_json)

        image_as_file = open(
            os.path.join(
                os.path.dirname(__file__),
                '../',
                'data',
                'image.png'
            ),
            "rb"
        )

        response, response_json = self.put_update(
            pipeline_data.get('id'),
            data={
                'file': image_as_file
            },
            action='process',
            _format='multipart',
        )
        self.assertEqual(response.status_code, 202, response_json)

        # Check result
        response, response_json = self.get_item(
            pk=response_json.get('id'),
            viewset=PipelineResultViewSet,
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertTrue(response_json['is_finished'], response_json)
        self.assertEqual(
            response_json['result']['url'],
            os.path.join(
                settings.MEDIA_URL,
                response_json['result']['id'],
            ),
            response_json
        )


class PipelinesProcessTestCase(PipelinesBaseTestCase):
    viewset = PipelineResultViewSet

    def setUp(self):
        super().setUp()

        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": "get_object_property",
                    "in_config": {
                        "property": "save_me"
                    }
                }
            ]
        }
        response, response_json = self.put_create(
            pipeline_data,
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 201, response_json)
        self.pipeline_id = response_json['id']

    @BaseTestCase.cases(
        ('string', 'test'),
        ('float', 1.2),
        ('int', 1),
        ('bool', True),
    )
    def test_pipeline_process_invalid_data(self, value):
        response, response_json = self.put_update(
            self.pipeline_id,
            {
                "data": {
                    value
                }
            },
            action='process',
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 400, response_json)
        self.assertIn(" is not of type 'object'", response_json)

    def test_pipeline_process_valid_data(self):
        response, response_json = self.put_update(
            self.pipeline_id,
            {
                "data": {
                    "save_me": 123
                },
            },
            action='process',
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], self.pipeline_id)

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertEqual(response_json['pipeline'], self.pipeline_id)
        self.assertTrue(response_json['is_finished'], response_json)
        self.assertEqual(response_json['result'], 123, response_json)

    def test_pipeline_process_valid_data_multiple_processors_json(self):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": "get_object_property",
                    "in_config": {
                        "property": "markdown_here"
                    }
                },
                {
                    "id": "markdown"
                }
            ]
        }
        response, response_json = self.put_create(
            pipeline_data,
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 201, response_json)

        pipeline_id = response_json['id']

        response, response_json = self.put_update(
            pipeline_id,
            {
                "data": {
                    "markdown_here": "**Hello World**"
                }
            },
            action='process',
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], pipeline_id)

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertTrue(response_json['is_finished'], response_json)
        self.assertEqual(response_json['result'], "<p><strong>Hello World</strong></p>\n", response_json)

    def test_pipeline_process_valid_data_multiple_processors_multipart(self):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": "resize_image",
                    "in_config": {
                        "size": [
                            200,
                            200
                        ]
                    },
                },
                {
                    "id": "watermark_image",
                    "in_config": {
                        "gravity": "SouthEast",
                        "watermark_image": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/146/thinking-face_1f914.png"
                    }
                }
            ]
        }
        response, response_json = self.put_create(
            pipeline_data,
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 201, response_json)

        pipeline_id = response_json['id']

        response, response_json = self.post_create(
            pk=pipeline_id,
            data={
                'file': open(
                    os.path.join(
                        os.path.dirname(__file__),
                        "../",
                        "data",
                        "image.png"
                    ),
                    "rb"
                )
            },
            action='process',
            viewset=PipelineViewSet,
            _format='multipart',
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], pipeline_id)

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertTrue(response_json['is_finished'], response_json)
        self.assertEqual(
            response_json['result']['url'],
            os.path.join(
                settings.MEDIA_URL,
                response_json['result']['id'],
            ),
            response_json
        )

    def test_pipeline_preview_json(self):
        """
            Sometimes it's necessary to "Preview" processors
                and data/file without saving the Pipeline
        """
        response, response_json = self.put_update(
            self.pipeline_id,
            {
                "data": {
                    "save_me": "123"
                },
                "processors": [
                    {
                        "id": "get_object_property",
                        "in_config": {
                            "property": "save_me"
                        }
                    },
                    {
                        "id": "md5"
                    }
                ]
            },
            action='process',
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], self.pipeline_id)

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertEqual(response_json['pipeline'], self.pipeline_id)
        self.assertTrue(response_json['is_finished'], response_json)
        self.assertEqual(
            response_json['result'],
            '202cb962ac59075b964b07152d234b70',
            response_json
        )

    def test_pipeline_preview_multipart(self):
        """
            Sometimes it's necessary to "Preview" processors
                and data/file without saving the Pipeline
        """
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": [
                {
                    "id": "resize_image",
                    "in_config": {
                        "size": [
                            200,
                            200
                        ]
                    },
                }
            ]
        }
        response, response_json = self.put_create(
            pipeline_data,
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 201, response_json)

        pipeline_id = response_json['id']

        response, response_json = self.post_create(
            pk=pipeline_id,
            data={
                'file': open(
                    os.path.join(
                        os.path.dirname(__file__),
                        "../",
                        "data",
                        "image.png"
                    ),
                    "rb"
                ),
                'processors': json.dumps([
                    {
                        "id": "resize_image",
                        "in_config": {
                            "size": [
                                200,
                                200
                            ]
                        },
                    },
                    {
                        "id": "watermark_image",
                        "in_config": {
                            "gravity": "SouthEast",
                            "watermark_image": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/146/thinking-face_1f914.png"
                        }
                    }
                ])
            },
            action='process',
            viewset=PipelineViewSet,
            _format='multipart',
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], pipeline_id)

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertTrue(response_json['is_finished'], response_json)
        self.assertEqual(
            response_json['result']['url'],
            os.path.join(
                settings.MEDIA_URL,
                response_json['result']['id'],
            ),
            response_json
        )

    @mock.patch('requests.request')
    def test_pipeline_web_hook_json(self, mocked_request):
        response = ""
        mocked_request.return_value = self._fake_http_response(
            status=200,
            json_data=response,
        )

        method = 'PUT'
        url = 'http://127.0.0.1'
        _data = {
            'save_me': '123'
        }

        response, response_json = self.put_update(
            self.pipeline_id,
            {
                "data": _data,
                "processors": [
                    {
                        "id": "get_object_property",
                        "in_config": {
                            "property": "save_me",
                        }
                    },
                    {
                        "id": "web_hook",
                        "in_config": {
                            "method": method,
                            "url": url,
                        }
                    }
                ]
            },
            action='process',
            viewset=PipelineViewSet
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], self.pipeline_id)

        mocked_request.assert_called()
        mocked_request.assert_called_with(
            method,
            url,
            data='123',
            files=None,
            headers={},
            timeout=(5, 5),
        )

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertTrue(response_json['is_finished'], response_json)
        self.assertEqual(response_json['result'], '123')

    @mock.patch('requests.request')
    def test_pipeline_web_hook_multipart(self, mocked_request):
        response = ""
        mocked_request.return_value = self._fake_http_response(
            status=200,
            json_data=response,
        )

        method = 'PUT'
        url = 'http://127.0.0.1'

        response, response_json = self.put_update(
            self.pipeline_id,
            {
                "file": open(
                    os.path.join(
                        os.path.dirname(__file__),
                        "../",
                        "data",
                        "image.png"
                    ),
                    "rb"
                ),
                "processors": json.dumps([
                    {
                        "id": "resize_image",
                        "in_config": {
                            "percentage": 15
                        }
                    },
                    {
                        "id": "web_hook",
                        "in_config": {
                            "method": method,
                            "url": url,
                        }
                    }
                ])
            },
            action='process',
            viewset=PipelineViewSet,
            _format='multipart',
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], self.pipeline_id)

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertTrue(response_json['is_finished'], response_json)

        mocked_request.assert_called_once()
        call_args = mocked_request.call_args
        self.assertEqual(
            call_args[0], (method, url)
        )

        payload = call_args[1]
        self.assertIsNone(payload['data'])
        self.assertIn('files', payload)
        self.assertEqual(
            payload['headers'], {'Content-type': 'multipart/form-data'}
        )
        self.assertEqual(payload['timeout'], (5, 5))
        self.assertIn(
            response_json['result']['id'],
            payload['files']['file'].name,
        )

    @mock.patch('requests.request')
    def test_pipeline_web_hook_multipart_consumed_by_file_processor(self, mocked_request):
        response = ""
        mocked_request.return_value = self._fake_http_response(
            status=200,
            json_data=response,
        )

        method = 'PUT'
        url = 'http://127.0.0.1'

        response, response_json = self.put_update(
            self.pipeline_id,
            {
                "file": open(
                    os.path.join(
                        os.path.dirname(__file__),
                        "../",
                        "data",
                        "image.png"
                    ),
                    "rb"
                ),
                "processors": json.dumps([
                    {
                        "id": "resize_image",
                        "in_config": {
                            "percentage": 15
                        }
                    },
                    {
                        "id": "web_hook",
                        "in_config": {
                            "method": method,
                            "url": url,
                        }
                    },
                    {
                        "id": "resize_image",
                        "in_config": {
                            "percentage": 15
                        }
                    },
                ])
            },
            action='process',
            viewset=PipelineViewSet,
            _format='multipart',
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], self.pipeline_id)

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertTrue(response_json['is_finished'], response_json)

        mocked_request.assert_called_once()

        self.assertEqual(
            response_json['result']['url'],
            os.path.join(
                settings.MEDIA_URL,
                response_json['result']['id'],
            ),
            response_json
        )

    @mock.patch('requests.request')
    def test_pipeline_web_hook_json_consumed_by_object_processor(self, mocked_request):
        response = ""
        mocked_request.return_value = self._fake_http_response(
            status=200,
            json_data=response,
        )

        method = 'PUT'
        url = 'http://127.0.0.1'

        response, response_json = self.put_update(
            self.pipeline_id,
            {
                "data": {
                    "save_me": 123
                },
                "processors": [
                    {
                        "id": "web_hook",
                        "in_config": {
                            "method": method,
                            "url": url,
                        }
                    },
                    {
                        "id": "get_object_property",
                        "in_config": {
                            "property": "save_me",
                        }
                    },
                ]
            },
            action='process',
            viewset=PipelineViewSet,
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], self.pipeline_id)

        mocked_request.assert_called_once()

        response, response_json = self.get_item(
            pk=response_json.get('id')
        )
        self.assertEqual(response.status_code, 200, response_json)
        self.assertIsNone(response_json['error'])
        self.assertTrue(response_json['is_finished'], response_json)
        self.assertEqual(response_json['result'], 123, response_json)
