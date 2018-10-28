from projects.workers.markdown import Markdown
from tests.base import BaseTestCase


class MarkdownTestCase(BaseTestCase):
    worker_class = Markdown

    @BaseTestCase.cases(
        ('string', '**Hello World**', '<p><strong>Hello World</strong></p>\n'),
    )
    def test_worker(self, value, expectation):
        result = self.worker_class().process(value)
        self.assertEqual(result, expectation)
