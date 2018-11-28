import base64
import filecmp
import os

from django.conf import settings
import rest_framework

from projects.models.pipeline import *
from projects.workers.watermark_image import WatermarkImage
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class WatermarkImageTestCase(WorkerBaseTestCase):
    worker_class = WatermarkImage

    data_location = os.path.join(
        os.path.dirname(__file__),
        '../',
        'data',
    )

    image_file_location = os.path.join(
        data_location,
        'image.png'
    )
    watermark_file_location = os.path.join(
        data_location,
        'watermark.png'
    )

    image_as_file = open(image_file_location, 'rb')
    watermark_as_file = open(watermark_file_location, 'rb')

    image_as_data = base64.b64encode(
        open(
            os.path.join(data_location, 'image.png'),
            'rb'
        ).read()
    ).decode()
    watermark_as_data = base64.b64encode(
        open(
            os.path.join(data_location, 'watermark.png'),
            'rb'
        ).read()
    ).decode()

    @BaseTestCase.cases(
        # Image File / WatermarkImage Base64
        (
            'file_image_with_base64_watermark_northwest',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'NorthWest'
            },
            image_as_file,
            'watermarked_northwest.png',
        ),
        (
            'file_image_with_base64_watermark_north',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'North'
            },
            image_as_file,
            'watermarked_north.png',
        ),
        (
            'file_image_with_base64_watermark_northeast',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'NorthEast'
            },
            image_as_file,
            'watermarked_northeast.png',
        ),
        (
            'file_image_with_base64_watermark_west',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'West'
            },
            image_as_file,
            'watermarked_west.png',
        ),
        (
            'file_image_with_base64_watermark_center',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'Center'
            },
            image_as_file,
            'watermarked_center.png',
        ),
        (
            'file_image_with_base64_watermark_east',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'East'
            },
            image_as_file,
            'watermarked_east.png',
        ),
        (
            'file_image_with_base64_watermark_southwest',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'SouthWest'
            },
            image_as_file,
            'watermarked_southwest.png',
        ),
        (
            'file_image_with_base64_watermark_south',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'South'
            },
            image_as_file,
            'watermarked_south.png',
        ),
        (
            'file_image_with_base64_watermark_southeast',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'SouthEast'
            },
            image_as_file,
            'watermarked_southeast.png',
        ),

        # Image Base64 / WatermarkImage Base64
        (
            'base64_image_with_base64_watermark_northwest',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'NorthWest'
            },
            image_as_data,
            'watermarked_northwest.png',
        ),
        (
            'base64_image_with_base64_watermark_north',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'North'
            },
            image_as_data,
            'watermarked_north.png',
        ),
        (
            'base64_image_with_base64_watermark_northeast',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'NorthEast'
            },
            image_as_data,
            'watermarked_northeast.png',
        ),
        (
            'base64_image_with_base64_watermark_west',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'West'
            },
            image_as_data,
            'watermarked_west.png',
        ),
        (
            'base64_image_with_base64_watermark_center',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'Center'
            },
            image_as_data,
            'watermarked_center.png',
        ),
        (
            'base64_image_with_base64_watermark_east',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'East'
            },
            image_as_data,
            'watermarked_east.png',
        ),
        (
            'base64_image_with_base64_watermark_southwest',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'SouthWest'
            },
            image_as_data,
            'watermarked_southwest.png',
        ),
        (
            'base64_image_with_base64_watermark_south',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'South'
            },
            image_as_data,
            'watermarked_south.png',
        ),
        (
            'base64_image_with_base64_watermark_southeast',
            {
                'watermark_image': watermark_as_data,
                'gravity': 'SouthEast'
            },
            image_as_data,
            'watermarked_southeast.png',
        ),

        # Image File / WatermarkImage File
        (
            'file_image_with_file_watermark_northwest',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'NorthWest'
            },
            image_as_file,
            'watermarked_northwest.png',
        ),
        (
            'file_image_with_file_watermark_north',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'North'
            },
            image_as_file,
            'watermarked_north.png',
        ),
        (
            'file_image_with_file_watermark_northeast',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'NorthEast'
            },
            image_as_file,
            'watermarked_northeast.png',
        ),
        (
            'file_image_with_file_watermark_west',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'West'
            },
            image_as_file,
            'watermarked_west.png',
        ),
        (
            'file_image_with_file_watermark_center',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'Center'
            },
            image_as_file,
            'watermarked_center.png',
        ),
        (
            'file_image_with_file_watermark_east',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'East'
            },
            image_as_file,
            'watermarked_east.png',
        ),
        (
            'file_image_with_file_watermark_southwest',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'SouthWest'
            },
            image_as_file,
            'watermarked_southwest.png',
        ),
        (
            'file_image_with_file_watermark_south',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'South'
            },
            image_as_file,
            'watermarked_south.png',
        ),
        (
            'file_image_with_file_watermark_southeast',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'SouthEast'
            },
            image_as_file,
            'watermarked_southeast.png',
        ),

        # Image Base64 / WatermarkImage File
        (
            'base64_image_with_file_watermark_northwest',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'NorthWest'
            },
            image_as_data,
            'watermarked_northwest.png',
        ),
        (
            'base64_image_with_file_watermark_north',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'North'
            },
            image_as_data,
            'watermarked_north.png',
        ),
        (
            'base64_image_with_file_watermark_northeast',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'NorthEast'
            },
            image_as_data,
            'watermarked_northeast.png',
        ),
        (
            'base64_image_with_file_watermark_west',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'West'
            },
            image_as_data,
            'watermarked_west.png',
        ),
        (
            'base64_image_with_file_watermark_center',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'Center'
            },
            image_as_data,
            'watermarked_center.png',
        ),
        (
            'base64_image_with_file_watermark_east',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'East'
            },
            image_as_data,
            'watermarked_east.png',
        ),
        (
            'base64_image_with_file_watermark_southwest',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'SouthWest'
            },
            image_as_data,
            'watermarked_southwest.png',
        ),
        (
            'base64_image_with_file_watermark_south',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'South'
            },
            image_as_data,
            'watermarked_south.png',
        ),
        (
            'base64_image_with_file_watermark_southeast',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'SouthEast'
            },
            image_as_data,
            'watermarked_southeast.png',
        ),

        # With size
        (
            'base64_image_with_file_watermark_southeast_and_size',
            {
                'watermark_image': watermark_as_file,
                'gravity': 'SouthEast',
                'size': {
                    'width': 220,
                    'height': 220,
                }
            },
            image_as_data,
            'watermarked_southeast.png',
        )
    )
    def test_worker(self, in_config, value, expectation):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={
                'id': 'watermark_image',
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
                os.path.join(
                    self.data_location,
                    expectation
                )
            ),
            file_id
        )
