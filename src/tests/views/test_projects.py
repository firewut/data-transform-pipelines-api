from projects.views import (
    ProjectsViewSet
)
from tests.base import BaseTestCase


class ProjectsTestCase(BaseTestCase):
    viewset = ProjectsViewSet

    def create_project(self, data: dict = None):
        if data is None:
            data = {
                'title': self.random_string(30),
                'description': self.random_string(100),
            }
        return self.post_create(data)

    def test_create_project(self):
        data = {
            'title': self.random_string(30),
            'description': self.random_string(100),
        }
        response = self.create_project(data)
        self.assertEqual(response.status_code, 201, response.data)
        for k, v in data.items():
            self.assertEqual(response.data[k], v)

    def test_create_project_with_pipelines(self):
        data = {
            'title': self.random_string(30),
            'description': self.random_string(100),
            'pipelines': [
                {
                    "id": self.random_uuid(),
                    "title": self.random_string(),
                    "processors": [
                        {
                            "id":  "md5"
                        }
                    ]
                }
            ]
        }
        response = self.create_project(data)
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data.get('pipelines'), [], response.data)

    def test_list_projects(self):
        projects = []
        num_projects = self.page_size + 1

        for _ in range(num_projects):
            projects.append(
                self.create_project()
            )
        self.assertEqual(len(projects), num_projects)

        response = self.get_list(self.viewset)
        self.assertEqual(response.status_code, 200)

        # Pagination
        self.assertIn('pagination', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(
            response.data['pagination']['count'],
            num_projects + 4
        )
        self.assertLess(len(response.data['results']), num_projects)
