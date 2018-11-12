import copy
import mock

from projects.workers.web_hook import Webhook
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class WebhookTestCase(WorkerBaseTestCase):
    worker_class = Webhook

    @BaseTestCase.cases(
        (
            'GET__headers__no_timeout',
            'GET',
            {'Authorization': 'Token blabla'},
            {},
        ),
        (
            'GET__no_headers__timeout',
            'GET',
            {},
            {'connect': 6, 'read': 7}
        ),
        (
            'GET__headers__timeout',
            'GET',
            {'Authorization': 'Token blabla2'},
            {'connect': 7, 'read': 8}
        ),
        (
            'GET__no_headers__no_timeout',
            'GET',
            {},
            {}
        ),
        (
            'POST__headers__no_timeout',
            'POST',
            {'Authorization': 'Token blabla'},
            {},
        ),
        (
            'POST__no_headers__timeout',
            'POST',
            {},
            {'connect': 6, 'read': 7}
        ),
        (
            'POST__headers__timeout',
            'POST',
            {'Authorization': 'Token blabla2'},
            {'connect': 7, 'read': 8}
        ),
        (
            'POST__no_headers__no_timeout',
            'POST',
            {},
            {}
        ),
        (
            'PUT__headers__no_timeout',
            'PUT',
            {'Authorization': 'Token blabla'},
            {},
        ),
        (
            'PUT__no_headers__timeout',
            'PUT',
            {},
            {'connect': 6, 'read': 7}
        ),
        (
            'PUT__headers__timeout',
            'PUT',
            {'Authorization': 'Token blabla2'},
            {'connect': 7, 'read': 8}
        ),
        (
            'PUT__no_headers__no_timeout',
            'PUT',
            {},
            {}
        ),
        (
            'PATCH__headers__no_timeout',
            'PATCH',
            {'Authorization': 'Token blabla'},
            {},
        ),
        (
            'PATCH__no_headers__timeout',
            'PATCH',
            {},
            {'connect': 6, 'read': 7}
        ),
        (
            'PATCH__headers__timeout',
            'PATCH',
            {'Authorization': 'Token blabla2'},
            {'connect': 7, 'read': 8}
        ),
        (
            'PATCH__no_headers__no_timeout',
            'PATCH',
            {},
            {}
        ),
        (
            'DELETE__headers__no_timeout',
            'DELETE',
            {'Authorization': 'Token blabla'},
            {},
        ),
        (
            'DELETE__no_headers__timeout',
            'DELETE',
            {},
            {'connect': 6, 'read': 7}
        ),
        (
            'DELETE__headers__timeout',
            'DELETE',
            {'Authorization': 'Token blabla2'},
            {'connect': 7, 'read': 8}
        ),
        (
            'DELETE__no_headers__no_timeout',
            'DELETE',
            {},
            {}
        ),
    )
    @mock.patch('requests.request')
    def test_worker(
        self,
        method,
        headers,
        timeout,
        mocked_request
    ):
        response = ""
        mocked_request.return_value = self._fake_http_response(
            status=200,
            json_data=response,
        )

        url = self.random_url()

        data = self.random_string(30)
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={
                'id': 'web_hook',
                'in_config': {
                    'url': url,
                    'method': method,
                    'headers': headers,
                    'timeout': timeout,
                },
            }
        ).execute(
            data
        )

        self.assertEqual(result, data)

        if timeout:
            _timeout = (
                timeout['connect'],
                timeout['read']
            )
        else:
            _timeout = (
                5,
                5,
            )

        mocked_request.assert_called()
        mocked_request.assert_called_with(
            method,
            url,
            data=data,
            headers=headers,
            timeout=_timeout,
        )

    @BaseTestCase.cases(
        ('none', None),
        ('data', 'data'),
    )
    @mock.patch('requests.request')
    def test_worker_payload_wrapper(
        self,
        payload_wrapper,
        mocked_request
    ):
        response = ""
        mocked_request.return_value = self._fake_http_response(
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
                    'payload_wrapper': payload_wrapper
                },
            }
        ).execute(
            data
        )

        self.assertEqual(result, data)

        _data = copy.deepcopy(data)
        if payload_wrapper:
            _data = {
                payload_wrapper: _data
            }

        mocked_request.assert_called()
        mocked_request.assert_called_with(
            method,
            url,
            data=_data,
            headers={},
            timeout=(5, 5),
        )
