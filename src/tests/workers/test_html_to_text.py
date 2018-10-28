from projects.workers.html_to_text import HTMLToText
from tests.base import BaseTestCase


class HTMLToTextTestCase(BaseTestCase):
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
        result = self.worker_class().process(value)
        self.assertEqual(result, expectation)
