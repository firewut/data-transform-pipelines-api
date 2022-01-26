from projects.workers.random_string import RandomString
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class RandomStringTestCase(WorkerBaseTestCase):
    worker_class = RandomString

    @BaseTestCase.cases(("string", {}, str))
    def test_worker(self, in_config, expectation_class):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={"id": "random_string", "in_config": in_config},
        ).execute()

        self.assertTrue(isinstance(result, expectation_class))
