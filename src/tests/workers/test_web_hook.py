import mock

from projects.workers.web_hook import WebHook
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class WebHookTestCase(WorkerBaseTestCase):
    worker_class = WebHook

    @mock.patch('requests.get')
    def test_worker_get(self, mocked_get):
        response = ""
        mocked_get.return_value = self._fake_http_response(
            status=200,
            json_data=response,
        )

        url = self.random_url()
        method = 'GET'

        data = self.random_string(30)
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={
                'id': 'web_hook',
                'in_config': {
                    'url': url,
                    'method': method,
                }
            }
        ).execute(
            data
        )

        self.assertEqual(result, data)

        mocked_get.assert_called()
        mocked_get.assert_called_with(
            url=url,
            method=method,
        )
