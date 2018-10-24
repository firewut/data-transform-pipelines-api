import copy

from projects.views import (
    PipelineViewSet
)
from tests.base import BaseTestCase


class PipelinesTestCase(BaseTestCase):
    viewset = PipelineViewSet

    def setUp(self):
        super().setUp()

        project_response, response_json = self.create_project({
            'title': self.random_string(30),
            'description': self.random_string(100),
        })
        self.assertEqual(project_response.status_code, 201)
        self.project_id = response_json['id']

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
        ('random_none', 'random', {"length": 10, "random_type": "string"}, None),
        ('random_empty', 'random', {"length": 10, "random_type": "string"}, {}),
        ('get_object_property_empty', 'get_object_property', {"property": "lala"}, {}),
        ('get_object_property_none', 'get_object_property', {"property": "lala"}, None),
        ('get_object_property', 'get_object_property', {"property": "lala"}, {"lala": "123"}),
        ('html_to_text_empty', 'html_to_text', {}, ""),
    )
    def test_processors_valid_input_data(self, processor_id, in_config, in_data):
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
            user=self.user,
            action='process'
        )
        self.assertEqual(response.status_code, 202, response_json)
        self.assertEqual(response_json['pipeline'], pipeline_data['id'])

        self.assertIn(
            'pipeline_results/{}/'.format(
                response_json.get('id')
            ),
            response['Location'],
        )
