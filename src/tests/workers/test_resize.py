import base64
import filecmp
import os

from django.conf import settings

from projects.models.pipeline import *
from projects.workers.resize import Resize
from tests.base import BaseTestCase


class ResizeTestCase(BaseTestCase):
    worker_class = Resize

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
            {'size': [100, 100]},
            image_as_file,
        ),
        (
            'base64_with_size',
            {'size': [100, 100]},
            image_as_data,
        ),
    )
    def test_worker(self, in_config, value):
        result = self.worker_class(
            pipeline_processor={
                'id': 'resize',
                'in_config': in_config
            }
        ).execute(
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
                self.resized_image_path,
            ),
            file_id
        )
