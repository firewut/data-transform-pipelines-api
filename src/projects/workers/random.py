
from core.utils import *
from projects.workers.base import Worker


class Random(Worker):
    id = 'random'
    name = 'random'
    image = 'https://upload.wikimedia.org/wikipedia/commons/e/e1/Ideal_chain_random_walk.png'
    description = 'Make a random value'
    ui_schema = {
        "ui:order": [
            "random_type", "*",
        ],
    }
    schema = {
        "type": "object",
        "required": [
                "in_config"
        ],
        "properties": {
            "in": {
                "type": "null",
                "description": "takes no input data"
            },
            "in_config": {
                "type": "object",
                "properties": {
                    "random_type": {
                        "type": "string",
                        "description": "Value Type",
                        "oneOf": [
                            {"title": "string", "enum": ["string"]},
                            {"title": "boolean", "enum": ["boolean"]},
                            {"title": "integer", "enum": ["integer"]},
                            {"title": "number", "enum": ["number"]},
                        ]
                    },
                    "length": {
                        "type": "integer",
                        "description": "for string"
                    },
                    "min": {
                        "type": "integer",
                        "description": "for number, integer",
                    },
                    "max": {
                        "type": "integer",
                        "description": "for number, integer",
                    }
                },
                "oneOf": [
                    {
                        "properties": {
                            "random_type": {
                                "type": "string",
                                "title": "boolean",
                                "enum": ["boolean"],
                            },
                        },
                        "additionalProperties": False,
                        "required": ["random_type"]
                    },
                    {
                        "properties": {
                            "random_type": {
                                "type": "string",
                                "enum": ["string"],
                            },
                            "length": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 100,
                            }
                        },
                        "additionalProperties": False,
                        "required": ["random_type", "length"]
                    },
                    {
                        "properties": {
                            "random_type": {
                                "type": "string",
                                "enum": ["number", "integer"],
                            },
                            "min": {
                                "type": "integer",
                                "minimum": 0,
                                "description": "Min",
                            },
                            "max": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "Max",
                            }
                        },
                        "additionalProperties": False,
                        "required": ["random_type"]
                    },
                ],
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
