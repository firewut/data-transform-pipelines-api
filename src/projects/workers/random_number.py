from core.utils import *
from projects.workers.base import Worker


class RandomNumber(Worker):
    id = "random_number"
    name = "random_number"
    image = "https://upload.wikimedia.org/wikipedia/commons/e/e1/Ideal_chain_random_walk.png"
    description = "Make a random Number"
    ui_schema = {
        "ui:order": ["random_type", "minimum", "maximum"],
    }
    schema = {
        "type": "object",
        "required": ["in_config"],
        "properties": {
            "in": {"type": "null", "description": "takes no input data"},
            "in_config": {
                "type": "object",
                "properties": {
                    "random_type": {
                        "type": "string",
                        "enum": ["number", "integer"],
                    },
                    "minimum": {
                        "type": "integer",
                        "description": "Minimum",
                    },
                    "maximum": {
                        "type": "integer",
                        "description": "Maximum",
                    },
                },
                "additionalProperties": False,
                "required": ["random_type"],
            },
            "in_config_example": {
                "random_type": "integer",
                "minimum": 10,
                "maximum": 200,
            },
            "out": {
                "description": "randomized number",
                "type": [
                    "number",
                    "integer",
                ],
            },
        },
    }

    def process(self, data=None):
        result = ""
        in_config = self.pipeline_processor.in_config

        random_type = in_config.get("random_type")
        if random_type == "number":
            result = random_float(
                in_config.get("minimum", 1), in_config.get("maximum", 1000000)
            )

        if random_type == "integer":
            result = random_int(
                in_config.get("minimum", 1), in_config.get("maximum", 1000000)
            )

        return result
