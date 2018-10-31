from readability import Document

from projects.workers.base import Worker


class Readability(Worker):
    id = 'readability'
    name = 'readability'
    image = 'data:image/png;base64,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'
    description = 'Makes an html readable'
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": [
                    "string"
                ],
                "description": "html to make readable"
            },
            "out": {
                "type": "object",
                "description": "output data",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "cleaned title"
                    },
                    "content": {
                        "type": "string",
                        "description": "cleaned content"
                    }
                }
            }
        }
    }

    def process(self, data):
        doc = Document(data)
        return {
            'title': doc.short_title(),
            'content': doc.summary()
        }
