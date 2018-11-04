import mock

from projects.workers.fetch_url import FetchURL
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class FetchURLTestCase(WorkerBaseTestCase):
    worker_class = FetchURL

    @mock.patch('requests.get')
    def test_worker(self, mocked_get):
        response = "html content <hr />"
        mocked_get.return_value = self._fake_http_response(
            status=200,
            json_data=response,
        )

        result = self.worker_class().execute(
            'https://example.com'
        )

        self.assertEqual(
            result,
            '"html content <hr />"'
        )
