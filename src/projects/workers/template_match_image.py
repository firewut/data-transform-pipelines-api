import os

from PIL import Image
import numpy as np
import cv2

from projects.workers.base import Worker
from projects.workers.exceptions import *


class TemplateMatchImage(Worker):
    id = 'template_match_image'
    name = 'template_match_image'
    image = ''
    description = 'Teampte Matching for Image'
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
                "description": "object to make a template from"
            },
            "in_config": {
                "type": "object",
                "required": [
                    "template_image",
                ],
                "properties": {
                    "template_image": {
                        "type": [
                            "file",
                            "string"
                        ],
                        "description": "Base64, URL or ID of a file uploaded recently"
                    },
                }
            },
            "in_config_example": {
                "template_image": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/146/thinking-face_1f914.png",
            },
            "out": {
                "type": "file",
                "description": "image with template highlighted"
            }
        }
    }

    def process(self, data):
        image = Image.open(data).convert("RGBA")

        if image is None:
            raise WorkerNoInputException(
                'File Object or Base64 String Input required'
            )

        in_config = self.pipeline_processor.in_config

        template_file = self.open_file(
            in_config['template_image']
        )

        if not template_file:
            raise WorkerInvalidInConfigException(
                'watermark is not available'
            )

        template = Image.open(
            template_file
        ).convert("RGBA")

        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv_template = cv2.cvtColor(np.array(template), cv2.COLOR_RGB2BGR)

        imageGray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        templateGray = cv2.cvtColor(cv_template, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        h, w = templateGray.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(cv_image, top_left, bottom_right, (0, 0, 255), 4)

        _file = self.request_file()
        filename = _file.path + '.png'
        cv2.imwrite(filename, cv_image)

        # Remove extension
        os.rename(filename, filename[:-4])

        image.close()
        template.close()

        return _file
