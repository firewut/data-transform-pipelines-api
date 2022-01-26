import base64
import filecmp
import os

from django.conf import settings
import rest_framework

from projects.models.pipeline import *
from projects.workers.grayscale_image import GrayscaleImage
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class GrayscaleImageTestCase(WorkerBaseTestCase):
    worker_class = GrayscaleImage

    grayscaled_image_path = os.path.join(
        WorkerBaseTestCase.images_dir, "grayscaled.png"
    )

    def test_worker__image_as_file(self):
        value = open(self.image_path, "rb")
        result = self.worker_class(pipeline_result=self.pipeline_result).execute(value)

        self.assertTrue(
            isinstance(result, rest_framework.utils.serializer_helpers.ReturnDict)
        )

        file_id = result["id"]

        self.assertTrue(
            filecmp.cmp(
                os.path.join(settings.MEDIA_ROOT, file_id + ".png"),
                self.grayscaled_image_path,
            ),
            file_id,
        )

    def test_worker__image_as_data(self):
        value = base64.b64encode(open(self.image_path, "rb").read()).decode()
        result = self.worker_class(pipeline_result=self.pipeline_result).execute(value)

        self.assertTrue(
            isinstance(result, rest_framework.utils.serializer_helpers.ReturnDict)
        )

        file_id = result["id"]

        self.assertTrue(
            filecmp.cmp(
                os.path.join(settings.MEDIA_ROOT, file_id + ".png"),
                self.grayscaled_image_path,
            ),
            file_id,
        )
