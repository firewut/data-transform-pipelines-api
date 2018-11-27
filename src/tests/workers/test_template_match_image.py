import base64
import filecmp
import os

from django.conf import settings
import rest_framework

from projects.models.pipeline import *
from projects.workers.template_match_image import TemplateMatchImage
from tests.workers.base import WorkerBaseTestCase


class TemplateMatchImageTestCase(WorkerBaseTestCase):
    worker_class = TemplateMatchImage

    data_location = os.path.join(
        os.path.dirname(__file__),
        '../',
        'data',
    )

    image_file_location = os.path.join(
        data_location,
        'watermarked_center.png'
    )

    template_file_location = os.path.join(
        data_location,
        'watermark.png'
    )

    image_as_file = open(image_file_location, 'rb')
    template_as_file = open(template_file_location, 'rb')

    image_as_data = base64.b64encode(
        open(
            os.path.join(data_location, 'watermarked_center.png'),
            'rb'
        ).read()
    ).decode()
    template_as_data = base64.b64encode(
        open(
            os.path.join(data_location, 'watermark.png'),
            'rb'
        ).read()
    ).decode()

    def test_worker(self):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={
                'id': 'template_match_image',
                'in_config': {
                    'template_image': self.template_as_data
                }
            }
        ).execute(
            self.image_as_data,
        )

        self.assertTrue(
            isinstance(
                result,
                rest_framework.utils.serializer_helpers.ReturnDict
            )
        )

        # Different Systems may generatee different image
        # file_id = result['id']
        # self.assertTrue(
        #     filecmp.cmp(
        #         os.path.join(
        #             settings.MEDIA_ROOT,
        #             file_id
        #         ),
        #         os.path.join(
        #             self.data_location,
        #             'template_matched_image.png'
        #         )
        #     ),
        #     "{} - {}".format(
        #         file_id,
        #         result
        #     )
        # )
