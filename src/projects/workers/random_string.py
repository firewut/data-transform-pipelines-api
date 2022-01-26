from core.utils import *
from projects.workers.base import Worker


class RandomString(Worker):
    id = "random_string"
    name = "random_string"
    image = "https://upload.wikimedia.org/wikipedia/commons/e/e1/Ideal_chain_random_walk.png"
    description = "Make a random String"
    ui_schema = {
        "ui:order": [
            "length",
            "alphabet",
        ],
    }

    schema = {
        "type": "object",
        "required": ["in_config"],
        "properties": {
            "in": {"type": "null", "description": "takes no input data"},
            "in_config": {
                "type": "object",
                "properties": {
                    "length": {"type": "integer", "description": "string length"},
                    "alphabet": {
                        "type": "string",
                        "description": "Use these characters",
                    },
                },
            },
            "in_config_example": {
                "length": "30",
            },
            "out": {
                "description": "randomized string",
                "type": [
                    "string",
                ],
            },
        },
    }

    def process(self, data=None):
        result = ""
        in_config = self.pipeline_processor.in_config

        result = random_string(
            in_config.get("length", 30),
            in_config.get("alphabet"),
        )

        return result
