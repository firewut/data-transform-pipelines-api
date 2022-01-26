from PIL import Image

from projects.workers.base import Worker
from projects.workers.exceptions import WorkerNoInputException


class ConvertImage(Worker):
    id = "convert_image"
    name = "convert_image"
    image = ""
    description = "Convert image from one format to another"

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
                "required": ["to"],
                "properties": {
                    "to": {
                        "type": "string",
                        "enum": [
                            "jpeg",
                            "png",
                        ],
                        "description": "Result Image Format",
                        "default": "jpeg",
                    }
                },
            },
            "in_config_example": {"to": "png"},
            "out": {"type": "file", "description": "resized file"},
        },
    }

    def process(self, data=None):
        image = Image.open(data)
        img = None

        if image is None:
            raise WorkerNoInputException("File Object or Base64 String Input required")

        in_config = self.pipeline_processor.in_config

        to = in_config.get("to")
        if to == "jpeg":
            img = image.convert("RGB")
            _format = "JPEG"

        if to == "png":
            img = image.convert("RGBA")
            _format = "PNG"

        _file = self.request_file()
        img.save(_file.path, _format)
        img.close()
        image.close()

        return _file
