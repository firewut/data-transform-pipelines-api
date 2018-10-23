import copy

from projects.views import (
    PipelineViewSet
)
from tests.base import BaseTestCase


class PipelinesTestCase(BaseTestCase):
    viewset = PipelineViewSet

    def setUp(self):
        super().setUp()

        project_response = self.create_project({
            'title': self.random_string(30),
            'description': self.random_string(100),
        })
        self.assertEqual(project_response.status_code, 201)
        self.project_id = project_response.data['id']

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

        response = self.post_create(pipeline_data)
        self.assertEqual(response.status_code, status_code, response.data)
        if status_code == 400:
            self.assertEqual(
                response.data,
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

        response = self.post_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response.data)

        response = self.post_create(pipeline_data)
        self.assertEqual(response.status_code, 409, response.data)

    def test_update_via_put(self):
        pipeline_data = {
            "id": self.random_uuid(),
            "title": self.random_string(),
            "project": self.project_id,
            "processors": []
        }

        response = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response.data)
        # data.get('id', data.get('pk'))
        response = self.put_update(
            pipeline_data.get('id'),
            pipeline_data
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_update_via_patch(self):
        pipeline_id = self.random_uuid()
        pipeline_data = {
            "id": pipeline_id,
            "title": self.random_string(),
            "project": self.project_id,
            "processors": []
        }

        response = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response.data)

        processors = [{'id': 'md5'}]
        _pipeline_data = copy.deepcopy(pipeline_data)
        _pipeline_data.update({
            'processors': processors
        })
        response = self.patch_update(
            _pipeline_data.get('id'),
            _pipeline_data
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['processors'][0]['id'], 'md5')

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

        response = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 201, response.data)

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

        response = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn(
            "readability[0] is incompatible with next processor google_translate",
            str(response.data),
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

        response = self.put_create(pipeline_data)
        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn(
            "random[0] has invalid in_config",
            str(response.data),
            response.data
        )
