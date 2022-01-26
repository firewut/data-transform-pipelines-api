from projects.views import ProjectsViewSet
from tests.base import BaseTestCase


class ProjectsTestCase(BaseTestCase):
    viewset = ProjectsViewSet

    def create_project(self, data: dict = None):
        if data is None:
            data = {
                "title": self.random_string(30),
                "description": self.random_string(100),
            }
        return self.post_create(data)

    def test_create_project(self):
        data = {
            "title": self.random_string(30),
            "description": self.random_string(100),
        }
        response, response_json = self.create_project(data)
        self.assertEqual(response.status_code, 201, response_json)
        for k, v in data.items():
            self.assertEqual(response_json[k], v)

    def test_create_project_with_pipelines(self):
        data = {
            "title": self.random_string(30),
            "description": self.random_string(100),
            "pipelines": [
                {
                    "id": self.random_uuid(),
                    "title": self.random_string(),
                    "processors": [{"id": "md5"}],
                }
            ],
        }
        response, response_json = self.create_project(data)
        self.assertEqual(response.status_code, 201, response_json)
        self.assertEqual(response_json.get("pipelines"), [], response_json)

    def test_list_projects(self):
        projects = []
        num_projects = self.page_size + 1

        for _ in range(num_projects):
            projects.append(self.create_project())
        self.assertEqual(len(projects), num_projects)

        response, response_json = self.get_list(self.viewset)
        self.assertEqual(response.status_code, 200)

        # Pagination
        self.assertIn("pagination", response_json)
        self.assertIn("results", response_json)
        self.assertEqual(response_json["pagination"]["count"], num_projects + 4)
        self.assertLess(len(response_json["results"]), num_projects)
