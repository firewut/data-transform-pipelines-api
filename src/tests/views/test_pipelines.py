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
        self.assertEqual(
            response.data['processors'],
            [{'id': 'md5'}]
        )
