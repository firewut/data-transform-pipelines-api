import base64
import filecmp
import os

from django.conf import settings
import rest_framework


from projects.models.pipeline import *
from projects.workers.convert_image import ConvertImage
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class ConvertImageTestCase(WorkerBaseTestCase):
    worker_class = ConvertImage

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

    @BaseTestCase.cases(
        (
            'png_jpeg',
            {'to': 'jpeg'},
            image_as_file,
            'image/jpeg'
        ),
        (
            'png_png',
            {'to': 'png'},
            image_as_file,
            'image/png'
        ),
    )
    def test_worker(self, in_config, value, assumed_mimetype):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={
                'id': 'convert_image',
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

        self.assertEqual(
            result['mimetype'], assumed_mimetype
        )
