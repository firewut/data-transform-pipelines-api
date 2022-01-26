import shutil

import requests

from projects.workers.base import Worker
from projects.workers.exceptions import *


class FetchURL(Worker):
    id = "fetch_url"
    name = "fetch_url"
    image = ""
    description = """
        Fetch URL Ccntent. Limitations:
          1. Uses HTTP GET Method
          2. Max of 3 redirects
          3. Max file size is 10Megabytes
    """
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": "string",
                "format": "url",
                "description": "URL to fetch content from",
            },
            "out": {"type": ["string", "null"], "description": "URL content"},
        },
    }

    def process(self, data):
        session = requests.Session()
        session.max_redirects = 3

        # ~10 Megabytes
        max_file_size = 10000000

        # OPTIONS request
        options = session.options(data)
        if "GET" not in options.headers.get("Allow"):
            raise WorkerNoInputException("Remote endpoint has no GET in Options")

        head = session.head(data)
        if int(head.headers.get("Content-Length", 0)) > max_file_size:
            raise WorkerNoInputException(
                "Remote endpoint response size exceeds 10 Megabytes"
            )

        response = session.get(data)
        response.raise_for_status()
        result = response.text

        return result
