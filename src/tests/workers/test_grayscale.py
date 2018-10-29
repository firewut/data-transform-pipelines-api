import base64
import filecmp
import os

from django.conf import settings

from projects.models.pipeline import *
from projects.workers.grayscale import Grayscale
from tests.base import BaseTestCase


class GrayscaleTestCase(BaseTestCase):
    worker_class = Grayscale

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

    grayscaled_image_path = os.path.join(
        os.path.dirname(__file__),
        '../',
        'data',
        'grayscaled.png'
    )

    @BaseTestCase.cases(
        (
            'file_with_size',
            image_as_file,
        ),
        (
            'base64_with_size',
            image_as_data,
        ),
    )
    def test_worker(self, value):
        result = self.worker_class().execute(
            value
        )
        file_id = result.id
        self.assertTrue(
            isinstance(result, PipelineResultFile)
        )

        self.assertTrue(
            filecmp.cmp(
                os.path.join(
                    settings.MEDIA_ROOT,
                    file_id
                ),
                self.grayscaled_image_path,
            ),
            file_id
        )
