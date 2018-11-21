from PIL import Image
import numpy

from projects.workers.base import Worker


class RandomImage(Worker):
    id = 'random_image'
    name = 'random_image'
    image = 'https://upload.wikimedia.org/wikipedia/commons/e/e1/Ideal_chain_random_walk.png'
    description = 'Make a random Image'
    ui_schema = {
        "ui:order": [
            "width", "height",
        ],
    }
    schema = {
        "type": "object",
        "required": [
                "in_config"
        ],
        "properties": {
            "in": {
                "type": "null",
                "description": "takes no input data"
            },
            "in_config": {
                "type": "object",
                "properties": {
                    "width": {
                        "type": "integer",
                        "minimum": 0,
                    },
                    "height": {
                        "type": "integer",
                        "minimum": 0,
                    }
                },
                "required": [
                    "width", "height"
                ]
            },
            "in_config_example": {
                "width": 100,
                "height": 100
            },
            "out": {
                "description": "randomized image",
                "type": "file",
            }
        }
    }

    def process(self, data=None):
        in_config = self.pipeline_processor.in_config

        width = in_config.get('width')
        height = in_config.get('height')

        imarray = numpy.random.rand(
            width,
            height,
            3
        ) * 255
        image = Image.fromarray(
            imarray.astype('uint8')
        ).convert('RGBA')

        _file = self.request_file()
        image.save(_file.path, 'png')
        image.close()

        return _file
