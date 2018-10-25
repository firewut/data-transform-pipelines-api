import jsonschema

from projects.models import *
from tests.base import BaseTestCase


class ProcessorsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.processor = Processor(
            schema={
                "id": "test",
                "type": "object",
                "properties": {
                    "in": {
                        "type": "integer"
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
                    }
                }
            }
        )

    @BaseTestCase.cases(
        ('string', '1'),
        ('float', 1.1),
        ('bool', False),
        ('none', None),
    )
    def test_check_input_data(self, value):
        self.processor.check_input_data(1)

        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.processor.check_input_data(value)

    def test_check_in_config(self):
        self.processor.check_in_config({
            "id": "test",
            "in_config": {
                "property": "extract_me"
            }
        })

        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.processor.check_in_config(None)

        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.processor.check_in_config({
                "id": "test"
            })

    def test_can_send_result(self):
        processor0 = Processor(
            schema={
                "type": "object",
                "properties": {
                    "in": {
                        "type": "integer"
                    },
                    "out": {
                        "type": "number"
                    }
                }
            }
        )
        processor1 = Processor(
            schema={
                "type": "object",
                "properties": {
                    "in": {
                        "type": "number"
                    },
                    "out": {
                        "type": "boolean"
                    }
                }
            }
        )

        # Correct Order
        self.assertTrue(
            processor0.can_send_result(processor1)
        )

        # Incorrect Order
        self.assertFalse(
            processor1.can_send_result(processor0)
        )
