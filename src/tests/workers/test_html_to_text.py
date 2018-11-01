from projects.workers.html_to_text import HTMLToText
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class HTMLToTextTestCase(WorkerBaseTestCase):
    worker_class = HTMLToText

    @BaseTestCase.cases(
        (
            '<a>',
            '<a>hello foo</a> bar',
            'hello foo bar'
        ),
        (
            '<div>',
            '<div>hello</div> foo <div>bar</div>',
            'hello foo bar'
        ),
        (
            'unclosed tag',
            '<div>hello</div> foo <div>bar',
            'hello foo bar'
        ),
        (
            'no_tags',
            'foo bar world',
            'foo bar world'
        ),
    )
    def test_worker(self, value, expectation):
        result = self.worker_class().execute(value)
        self.assertEqual(result, expectation)
