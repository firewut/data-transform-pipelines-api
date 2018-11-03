from core.utils import dict_finder
from projects.workers.base import Worker


class GetObjectProperty(Worker):
    id = 'get_object_property'
    name = 'get_object_property'
    image = None
    description = 'Get Object Property if exists'
    schema = {
        "type": "object",
        "required": [
                "in_config"
        ],
        "properties": {
            "in": {
                "type": "object"
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
                ]
            },
            "in_config": {
                "type": "object",
                "required": [
                        "property"
                ],
                "properties": {
                    "property": {
                        "type": "string"
                    }
                }
            },
            "in_config_example": {
                "property": "a.b.c"
            }
        }
    }

    def process(self, data):
        _property = self.pipeline_processor.in_config.get(
            'property'
        )

        return dict_finder(data, _property)
