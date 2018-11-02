from projects.workers.base import Worker


class Watermark(Worker):
    id = 'watermark'
    name = 'watermark'
    image = 'data:image/png;base64,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'
    description = 'Watermark an image'
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
                "required": [
                        "watermark_image",
                        "gravity"
                ],
                "properties": {
                    "watermark_image": {
                        "type": [
                            "file",
                            "string"
                        ],
                        "description": "Watermark file to apply"
                    },
                    "gravity": {
                        "type": "string",
                        "enum": [
                                "NorthWest",
                                "North",
                                "NorthEast",
                                "West",
                                "Center",
                                "East",
                                "SouthWest",
                                "South",
                                "SouthEast"
                        ],
                        "description": "watermark position"
                    }
                }
            },
            "in_config_example": {
                "watermark_image": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/146/thinking-face_1f914.png",
                "gravity": "SouthEast"
            },
            "out": {
                "type": "file",
                "description": "watermarked image"
            }
        }
    }

    def process(self, data):
        return data
