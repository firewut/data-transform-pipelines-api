
from core.utils import *
from projects.workers.base import Worker


class Random(Worker):
    id = 'random'
    name = 'random'
    image = 'https://upload.wikimedia.org/wikipedia/commons/e/e1/Ideal_chain_random_walk.png'
    description = 'Make a random value'
    schema = {
        "type": "object",
        "required": [
                "in_config"
        ],
        "properties": {
            "in": {
                "type": [
                    "null",
                    "object"
                ],
                "description": "takes no input data"
            },
            "in_config": {
                "type": "object",
                "oneOf": [
                    {
                        "properties": {
                            "random_type": {
                                "type": "string",
                                "enum": ["boolean"]
                            },
                        },
                        "additionalProperties": False,
                        "required": ["random_type"]
                    },
                    {
                        "properties": {
                            "random_type": {
                                "type": "string",
                                "enum": ["string"]
                            },
                            "length": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 100
                            }
                        },
                        "additionalProperties": False,
                        "required": ["random_type", "length"]
                    },
                    {
                        "properties": {
                            "random_type": {
                                "type": "string",
                                "enum": ["number", "integer"]
                            },
                            "min": {
                                "description": "valid for string, number, integer",
                                "type": "integer",
                                "minimum": 0
                            },
                            "max": {
                                "description": "valid for string, number, integer",
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 1000000
                            }
                        },
                        "additionalProperties": False,
                        "required": ["random_type"]
                    },
                ]
            },
            "in_config_example": {
                "random_type": "number",
                "min": 1,
                "max": 10
            },
            "out": {
                "description": "randomized result",
                "type": [
                    "string",
                    "boolean",
                    "number",
                    "integer"
                ]
            }
        }
    }

    def process(self, data=None):
        result = ''
        in_config = self.pipeline_processor.in_config

        random_type = in_config.get('random_type')
        if random_type == 'string':
            result = random_string(
                in_config.get('length', 50),
            )

        if random_type == 'number':
            result = random_float(
                in_config.get('min', 1),
                in_config.get('max', 1000000)
            )

        if random_type == 'boolean':
            result = random_bool()

        if random_type == 'integer':
            result = random_int(
                in_config.get('min', 1),
                in_config.get('max', 1000000)
            )

        return result
