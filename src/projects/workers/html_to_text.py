import re

from projects.workers.base import Worker


class HTMLToText(Worker):
    id = 'html_to_text'
    name = 'html_to_text'
    image = 'https://upload.wikimedia.org/wikipedia/sr/3/34/HTML5_Logo_256.png'
    description = 'Remove html tags from text'
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": "string",
                "description": "html to make a text from"
            },
            "out": {
                "type": [
                    "string",
                    "null"
                ],
                "description": "plain text"
            }
        }
    }

    def process(self, data):
        return re.sub(
            re.compile('<.*?>'),
            '',
            data
        )
