import jsonschema

from projects.workers.md5 import Md5
from tests.base import BaseTestCase


class Md5TestCase(BaseTestCase):
    worker_class = Md5

    @BaseTestCase.cases(
        ('integer', 123, None),
        ('string', '123', '202cb962ac59075b964b07152d234b70'),
        ('boolean', True, None),
        ('dict', {1: 2}, None),
    )
    def test_worker(self, value, expectation):
        if expectation:
            result = self.worker_class().execute(value)
            self.assertEqual(result, expectation)
        else:
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                self.worker_class().execute(value)
