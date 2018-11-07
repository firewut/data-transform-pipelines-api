import copy

import requests

from projects.workers.base import Worker


class WebHook(Worker):
    id = 'web_hook'
    name = 'web_hook'
    image = ''
    description = 'Triggers with ANY Data passed'
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": [
                    "array",
                    "boolean",
                    "integer",
                    "null",
                    "number",
                    "object",
                    "string",
                ],
                "description": "Input data as a Payload"
            },
            "in_config": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": [
                            "null", "string"
                        ],
                        "description": "ID of a Hook. Included to X-Hook-ID header of a Request"
                    },
                    "payload_wrapper": {
                        "type": [
                            "string", "null",
                        ],
                        "description": "If you need to move a payload into Root"
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "pattern": "^(http[s]?):\/\/"
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
                            "get",
                            "head",
                            "options",
                            "patch",
                            "post",
                            "put",
                        ]
                    },
                    "headers": {
                        "type": [
                            "null", "object",
                        ]
                    },
                    "timeout": {
                        "type": [
                            "object", "null",
                        ],
                        "properties": {
                            "read": {
                                "type": "number",
                                "format": "integer",
                                "min": 1,
                                "max": 60,
                                "default": 5,
                            },
                            "connect": {
                                "type": "number",
                                "format": "integer",
                                "min": 1,
                                "max": 60,
                                "default": 5,
                            }
                        },
                        "required": [
                            "read", "connect"
                        ],
                        "description": "timeout settings"
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
                    "method", "url",
                ]
            },
            "out": {
                "type": [
                    "array",
                    "boolean",
                    "integer",
                    "null",
                    "number",
                    "object",
                    "string",
                ],
                "description": "Equals to Input data"
            }
        }
    }

    def process(self, data):
        _data = data
        try:
            _data = copy.deepcopy(data)
        except Exception as e:
            pass

        in_config = self.pipeline_processor.in_config

        payload_wrapper = in_config.get('payload_wrapper')
        if payload_wrapper and isinstance(payload_wrapper, str):
            _data = {
                payload_wrapper: data
            }

        method = in_config.get('method', 'GET').upper()
        url = in_config.get('url')
        headers = in_config.get('headers', {})

        if 'id' in in_config:
            headers.update({
                'X-Hook-ID': in_config.get['id']
            })

        timeout = in_config.get('timeout', {})
        timeout_read = timeout.get('read', 5)
        timeout_connect = timeout.get('connect', 5)

        request = requests.request(
            method,
            url,
            data=_data,
            headers=headers,
            timeout=(
                timeout_connect,
                timeout_read,
            ),
        )

        return data
