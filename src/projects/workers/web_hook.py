import copy

import requests

from projects.workers.base import Worker


class Webhook(Worker):
    id = "web_hook"
    name = "web_hook"
    image = ""
    description = "Triggers with ANY Data passed"
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": [
                    "array",
                    "boolean",
                    "file",
                    "integer",
                    "null",
                    "number",
                    "object",
                    "string",
                ],
                "description": "Input data as a Payload",
            },
            "in_config": {
                "type": "object",
                "properties": {
                    "x-hook-id": {
                        "type": ["null", "string"],
                        "description": "ID of a Hook. Included to X-Hook-ID header of a Request",
                    },
                    "payload_wrapper": {
                        "type": [
                            "null",
                            "string",
                        ],
                        "description": "If you need to move a payload into Root. Does not Work with `file`",
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "pattern": "^(http[s]?):\/\/",
                    },
                    "method": {
                        "type": "string",
                        "enum": [
                            "GET",
                            "HEAD",
                            "OPTIONS",
                            "PATCH",
                            "POST",
                            "PUT",
                        ],
                    },
                    "headers": {
                        "type": [
                            "null",
                            "object",
                        ],
                        "properties": {},
                        "additionalProperties": True,
                    },
                    "timeout": {
                        "type": [
                            "null",
                            "object",
                        ],
                        "properties": {
                            "read": {
                                "type": "integer",
                                "min": 1,
                                "max": 60,
                                "default": 5,
                            },
                            "connect": {
                                "type": "integer",
                                "min": 1,
                                "max": 60,
                                "default": 5,
                            },
                        },
                        "additionalProperties": False,
                        "required": ["read", "connect"],
                        "description": "timeout settings",
                    },
                    # "retry": {
                    #     "type": [
                    #         "string",
                    #         "null",
                    #     ],
                    #     "enum": [
                    #         # "exponential",
                    #         "linear"
                    #     ],
                    #     "description": "Retry Strategy. Linear - 5 attempts every 5 seconds"
                    # }
                },
                "required": [
                    "method",
                    "url",
                ],
            },
            "in_config_example": {"method": "GET", "url": "http://example.com"},
            "out": {
                "type": [
                    "array",
                    "boolean",
                    "file",
                    "integer",
                    "null",
                    "number",
                    "object",
                    "string",
                ],
                "description": "Equals to Input data",
            },
        },
    }

    def process(self, data):
        _files = None
        try:
            _data = copy.deepcopy(data)
        except Exception as e:
            _data = data

        in_config = self.pipeline_processor.in_config

        method = in_config.get("method", "GET").upper()
        url = in_config.get("url")
        headers = in_config.get("headers", {})

        if self.input_is_file:
            _files = {"file": _data}
            _data = None
            headers.update({"Content-type": "multipart/form-data"})
        else:
            payload_wrapper = in_config.get("payload_wrapper")
            if payload_wrapper and isinstance(payload_wrapper, str):
                _data = {payload_wrapper: data}

        if "x-hook-id" in in_config:
            headers.update({"X-Hook-ID": in_config.get["x-hook-id"]})

        timeout = in_config.get("timeout", {})
        timeout_read = timeout.get("read", 5)
        timeout_connect = timeout.get("connect", 5)

        request = requests.request(
            method,
            url,
            data=_data,
            files=_files,
            headers=headers,
            timeout=(
                timeout_connect,
                timeout_read,
            ),
        )

        return data
