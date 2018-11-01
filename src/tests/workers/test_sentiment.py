from projects.workers.sentiment import Sentiment
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class SentimentTestCase(WorkerBaseTestCase):
    worker_class = Sentiment

    @BaseTestCase.cases(
        ('negative', 'wtf are you doing?', -0.5),
        ('neutral', 'test', 0.0),
        ('positive', 'The best', 1),
    )
    def test_worker(self, value, expectation):
        result = self.worker_class().execute(value)
        self.assertEqual(result, expectation)
