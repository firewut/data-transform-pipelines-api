import base64
import io
import os

from django.conf import settings
from PIL import Image

from core.utils import random_uuid4
from projects.workers.base import Worker
from projects.workers.exceptions import WorkerNoInputException


class GrayscaleImage(Worker):
    id = 'grayscale_image'
    name = 'grayscale_image'
    image = 'data:image/png;base64,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'
    description = 'Make an image grayscaled'
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": [
                    "file",
                    "string"
                ],
                "description": "object to make a template from"
            },
            "out": {
                "type": "file",
                "description": "output data"
            }
        }
    }

    def process(self, data):
        image = Image.open(data).convert('LA')
        if image is None:
            raise WorkerNoInputException(
                'File Object or Base64 String Input required'
            )

        _file = self.request_file()
        image.save(_file.path, 'png')
        image.close()

        return _file
