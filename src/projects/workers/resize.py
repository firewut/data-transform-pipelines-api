import base64
import io
import os

from django.conf import settings
from PIL import Image
from resizeimage import resizeimage

from core.utils import random_uuid4
from projects.workers.base import Worker
from projects.workers.exceptions import WorkerNoInputException


class Resize(Worker):
    id = 'resize'
    name = 'resize'
    image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Resize_small_font_awesome.svg/512px-Resize_small_font_awesome.svg.png'
    description = 'Resize an image'
    schema = {
        "type": "object",
        "required": [
                "in_config"
        ],
        "properties": {
            "in": {
                "type": [
                    "file",
                    "string"
                ],
                "title": "input data",
                "description": "object to make a template from"
            },
            "in_config": {
                "type": "object",
                "properties": {
                    # "percentage": {
                    #     "type": "number",
                    #     "title": "size",
                    #     "description": "size in percents",
                    #     "minimum": 0.01,
                    #     "maximum": 100
                    # },
                    "size": {
                        "type": "array",
                        "title": "size",
                        "description": "size in pixels",
                        "items": {
                            "title": "pixels",
                            "type": "integer",
                            "minimum": -1,
                            "maximum": 10000
                        },
                        "minItems": 2,
                        "maxItems": 2
                    }
                }
            },
            "in_config_example": {
                "percentage": 75
            },
            "out": {
                "type": "file",
                "description": "resized file"
            }
        }
    }

    def process(self, data):
        self.processor.check_input_data(data)

        in_config = self.pipeline_processor.in_config
        size = in_config.get('size')

        # Base64 image
        image = None
        if isinstance(data, str):
            image = Image.open(
                io.BytesIO(
                    base64.b64decode(data)
                )
            )

        # File like object
        if isinstance(data, io.BufferedReader):
            image = Image.open(data)

        if image is None:
            raise WorkerNoInputException(
                'File Object or Base64 String Input required'
            )

        img = resizeimage.resize_thumbnail(image, size)

        file_id = random_uuid4()
        file_path = os.path.join(
            settings.MEDIA_ROOT,
            file_id,
        )

        img.save(file_path, img.format)
        image.close()

        return file_id
