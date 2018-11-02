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
                    "percentage": {
                        "type": "integer",
                        "title": "size",
                        "description": "size in percents",
                        "minimum": 0.01,
                        "maximum": 100
                    },
                    "size": {
                        "type": "array",
                        "title": "size",
                        "description": "size in pixels",
                        "items": {
                            "title": "pixels",
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 10000
                        },
                        "minItems": 2,
                        "maxItems": 2
                    }
                },
                "oneOf": [
                    {
                        "required": ["percentage"]
                    },
                    {
                        "required": ["size"]
                    }
                ]
            },
            "in_config_example": {
                "size": [100, 100]
            },
            "out": {
                "type": "file",
                "description": "resized file"
            }
        }
    }

    def process(self, data):
        image = Image.open(data)
        img = None

        if image is None:
            raise WorkerNoInputException(
                'File Object or Base64 String Input required'
            )

        in_config = self.pipeline_processor.in_config

        percentage = None
        size = in_config.get('size')
        if size:
            img = resizeimage.resize_thumbnail(
                image,
                in_config.get('size')
            )
        else:
            percentage = int(in_config.get('percentage'))
            new_size = [
                (image.width * percentage) // 100,
                (image.width * percentage) // 100
            ]

            img = resizeimage.resize_thumbnail(
                image,
                new_size
            )

        _file = self.request_file()
        img.save(_file.path, img.format)
        image.close()

        return _file
