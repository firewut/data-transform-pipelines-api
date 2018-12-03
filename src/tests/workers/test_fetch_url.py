import mock
import json

import rest_framework

from projects.workers.exceptions import *
from projects.workers.fetch_url import FetchURL
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class FetchURLTestCase(WorkerBaseTestCase):
    worker_class = FetchURL

    @mock.patch('requests.Session.get')
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

    @mock.patch('requests.Session.options')
    def test_worker_no_methods(
        self,
        mocked_options
    ):
        mocked_options.return_value = self._fake_http_response(
            status=200,
            headers={
                'Allow': 'POST'
            }
        )

        with self.assertRaises(WorkerNoInputException):
            self.worker_class().execute(
                'https://example.com'
            )

    @mock.patch('requests.Session.options')
    @mock.patch('requests.Session.head')
    def test_worker_content_too_big(
        self,
        mocked_head,
        mocked_options
    ):
        mocked_options.return_value = self._fake_http_response(
            status=200,
            headers={
                'Allow': ['GET', 'HEAD']
            }
        )
        mocked_head.return_value = self._fake_http_response(
            status=200,
            headers={
                'Content-Length': 10000000 + 1
            }
        )

        with self.assertRaises(WorkerNoInputException):
            self.worker_class().execute(
                'https://example.com'
            )

    @mock.patch('requests.Session.options')
    @mock.patch('requests.Session.head')
    @mock.patch('requests.Session.get')
    def test_worker_meets_json(
        self,
        mocked_get,
        mocked_head,
        mocked_options
    ):
        json_data = json.dumps({'a': 'b'})

        mocked_options.return_value = self._fake_http_response(
            status=200,
            headers={
                'Allow': ['GET', 'HEAD']
            }
        )
        mocked_head.return_value = self._fake_http_response(
            status=200,
            headers={
                'Content-Type': 'application/json'
            }
        )
        mocked_get.return_value = self._fake_http_response(
            status=200,
            json_data=json_data
        )

        response = self.worker_class().execute(
            'https://example.com'
        )

        result = self.worker_class().execute(
            'https://example.com'
        )

        self.assertEqual(json.loads(result), json_data)

    @mock.patch('requests.Session.options')
    @mock.patch('requests.Session.head')
    @mock.patch('requests.Session.get')
    def test_worker_meets_csv(
        self,
        mocked_get,
        mocked_head,
        mocked_options
    ):
        json_data = "a,b,c"

        mocked_options.return_value = self._fake_http_response(
            status=200,
            headers={
                'Allow': ['GET', 'HEAD']
            }
        )
        mocked_head.return_value = self._fake_http_response(
            status=200,
            headers={
                'Content-Type': 'text/csv'
            }
        )
        mocked_get.return_value = self._fake_http_response(
            status=200,
            json_data=json_data
        )

        result = self.worker_class().execute(
            'https://example.com'
        )

        self.assertTrue(isinstance(result, str))
