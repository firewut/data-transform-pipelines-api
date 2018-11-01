from projects.workers.markdown import Markdown
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class MarkdownTestCase(WorkerBaseTestCase):
    worker_class = Markdown

    @BaseTestCase.cases(
        ('string', '**Hello World**', '<p><strong>Hello World</strong></p>\n'),
    )
    def test_worker(self, value, expectation):
        result = self.worker_class().execute(value)
        self.assertEqual(result, expectation)
