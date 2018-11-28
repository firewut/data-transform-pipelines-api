import base64
import filecmp
import os

from django.conf import settings
import rest_framework


from projects.models.pipeline import *
from projects.workers.resize_image import ResizeImage
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class ResizeImageTestCase(WorkerBaseTestCase):
    worker_class = ResizeImage

    image_as_file = open(
        os.path.join(
            os.path.dirname(__file__),
            '../',
            'data',
            'image.png'
        ),
        'rb'
    )
    image_as_data = base64.b64encode(
        open(
            os.path.join(
                os.path.dirname(__file__),
                '../',
                'data',
                'image.png'
            ),
            'rb'
        ).read()
    ).decode()

    # Always 100x100
    resized_image_path = os.path.join(
        os.path.dirname(__file__),
        '../',
        'data',
        'resized.png'
    )

    @BaseTestCase.cases(
        (
            'file_with_size',
            {'size': {'width': 100, 'height': 100}},
            image_as_file,
        ),
        (
            'base64_with_size',
            {'size': {'width': 100, 'height': 100}},
            image_as_data,
        ),
        (
            'file_with_percentage',
            {'percentage': 20},
            image_as_file,
        ),
        (
            'base64_with_percentage',
            {'percentage': 20},
            image_as_data,
        ),
    )
    def test_worker(self, in_config, value):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={
                'id': 'resize_image',
                'in_config': in_config
            }
        ).execute(
            value
        )

        self.assertTrue(
            isinstance(
                result,
                rest_framework.utils.serializer_helpers.ReturnDict
            )
        )

        file_id = result['id']

        self.assertTrue(
            filecmp.cmp(
                os.path.join(
                    settings.MEDIA_ROOT,
                    file_id + '.png'
                ),
                self.resized_image_path,
            ),
            file_id
        )

    def test_worker_invalid_file_type(self):
        text_as_data = 'TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCBieSB0aGlzIHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxzLCB3aGljaCBpcyBhIGx1c3Qgb2YgdGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZXZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGludWVkIGFuZCBpbmRlZmF0aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRoZSBzaG9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4='

        with self.assertRaises(OSError):
            result = self.worker_class(
                pipeline_result=self.pipeline_result,
                pipeline_processor={
                    'id': 'resize_image',
                    'in_config': {'percentage': 20},
                }
            ).execute(
                text_as_data
            )
