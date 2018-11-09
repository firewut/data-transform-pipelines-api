from projects.workers.base import Worker


class GoogleTranslate(Worker):
    id = 'google_translate'
    name = 'google_translate'
    image = 'https://upload.wikimedia.org/wikipedia/ru/a/a9/Google-Translate-icon.png'
    description = 'Translate text from one language to another language'
    schema = {
        "type": "object",
        "required": [
                "in_config"
        ],
        "properties": {
            "in": {
                "type": "string",
                "description": "Text to translate",
                "maxLength": 5000
            },
            "in_config": {
                "type": "object",
                "required": [
                        "from",
                        "to",
                        "api_key"
                ],
                "properties": {
                    "from": {
                        "type": "string",
                        "description": "From Language"
                    },
                    "to": {
                        "type": "string",
                        "description": "To Language"
                    },
                    "api_key": {
                        "type": "string",
                        "description": "Your Developer API Key"
                    }
                }
            },
            "in_config_example": {
                "from": "ru",
                "to": "en",
                "api_key": "<YOUR_API_KEY>"
            },
            "out": {
                "type": "string",
                "description": "output data"
            }
        }
    }

    def process(self, data):
        result = ""

        return result
