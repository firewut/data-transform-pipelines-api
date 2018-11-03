import requests

from projects.workers.base import Worker


class FetchURL(Worker):
    id = 'fetch_url'
    name = 'fetch_url'
    image = ''
    description = 'Fetch URL Content'
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": "string",
                "format": "url",
                "description": "URL to fetch content from"
            },
            "out": {
                "type": [
                    "string",
                    "null"
                ],
                "description": "URL Content"
            }
        }
    }

    def process(self, data):
        response = requests.get(data)
        response.raise_for_status()

        return response.text
