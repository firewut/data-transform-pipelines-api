from projects.workers.random_image import RandomImage
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class RandomImageTestCase(WorkerBaseTestCase):
    worker_class = RandomImage

    @BaseTestCase.cases(("image", {"width": 100, "height": 300}, dict))
    def test_worker(self, in_config, expectation_class):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={"id": "random_image", "in_config": in_config},
        ).execute()

        self.assertTrue(isinstance(result, expectation_class))
