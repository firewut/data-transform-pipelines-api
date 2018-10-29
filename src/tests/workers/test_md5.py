from projects.workers.md5 import Md5
from tests.base import BaseTestCase


class Md5TestCase(BaseTestCase):
    worker_class = Md5

    @BaseTestCase.cases(
        ('integer', 123, '202cb962ac59075b964b07152d234b70'),
        ('string', '123', '202cb962ac59075b964b07152d234b70'),
        ('boolean', True, 'f827cf462f62848df37c5e1e94a4da74'),
        ('dict', {1: 2}, '58df22b654b41dfbb0add72d96ce9982'),
    )
    def test_worker(self, value, expectation):
        result = self.worker_class().execute(value)
        self.assertEqual(result, expectation)
