from projects.workers.random_number import RandomNumber
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class RandomNumberTestCase(WorkerBaseTestCase):
    worker_class = RandomNumber

    @BaseTestCase.cases(
        ("integer", {"random_type": "integer"}, int),
        ("number", {"random_type": "number"}, float),
    )
    def test_worker(self, in_config, expectation_class):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={"id": "random_string", "in_config": in_config},
        ).execute()

        self.assertTrue(isinstance(result, expectation_class))
