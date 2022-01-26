from PIL import Image
from resizeimage import resizeimage

from projects.workers.base import Worker
from projects.workers.exceptions import WorkerNoInputException


class ResizeImage(Worker):
    id = "resize_image"
    name = "resize_image"
    image = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Resize_small_font_awesome.svg/512px-Resize_small_font_awesome.svg.png"
    description = "Resize an image. Tolerates Aspect Ratio"
    schema = {
        "type": "object",
        "required": ["in_config"],
        "properties": {
            "in": {
                "type": ["file", "string"],
                "description": "object to make a template from",
            },
            "in_config": {
                "type": "object",
                "properties": {
                    "size": {
                        "type": "object",
                        "description": "size in pixels",
                        "orderable": False,
                        "properties": {
                            "width": {
                                "type": "integer",
                                "minimum": 0,
                            },
                            "height": {
                                "type": "integer",
                                "minimum": 0,
                            },
                            "additionalProperties": False,
                        },
                        "required": ["width", "height"],
                    },
                    "percentage": {
                        "type": "integer",
                        "description": "size in percents",
                        "minimum": 0,
                    },
                },
                "oneOf": [
                    {"required": ["size"]},
                    {"required": ["percentage"]},
                ],
            },
            "in_config_example": {"size": {"width": 400, "height": 400}},
            "out": {"type": "file", "description": "resized file"},
        },
    }

    def process(self, data):
        image = Image.open(data)
        img = None

        if image is None:
            raise WorkerNoInputException("File Object or Base64 String Input required")

        in_config = self.pipeline_processor.in_config

        percentage = None
        size = in_config.get("size")
        if size:
            img = resizeimage.resize_thumbnail(
                image, [size.get("width"), size.get("height")]
            )
        else:
            percentage = int(in_config.get("percentage"))
            new_size = [
                (image.width * percentage) // 100,
                (image.height * percentage) // 100,
            ]

            img = resizeimage.resize_thumbnail(image, new_size)

        _file = self.request_file()
        img.save(_file.path, img.format)
        image.close()

        return _file
