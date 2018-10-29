from projects.workers.sentiment import Sentiment
from tests.base import BaseTestCase


class SentimentTestCase(BaseTestCase):
    worker_class = Sentiment

    @BaseTestCase.cases(
        ('negative', 'wtf are you doing?', -0.5),
        ('neutral', 'test', 0.0),
        ('positive', 'The best', 1),
    )
    def test_worker(self, value, expectation):
        result = self.worker_class().execute(value)
        self.assertEqual(result, expectation)
