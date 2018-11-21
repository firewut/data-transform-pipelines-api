from projects.workers.random import Random
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class RandomTestCase(WorkerBaseTestCase):
    worker_class = Random

    @BaseTestCase.cases(
        ('integer', {'random_type': 'integer'}, int),
        ('string', {'random_type': 'string'}, str),
        ('boolean', {'random_type': 'boolean'}, bool),
        ('number', {'random_type': 'number'}, float),
        ('image', {'random_type': 'image', 'width': 100, 'height': 300}, dict)
    )
    def test_worker(self, in_config, expectation_class):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={
                'id': 'random',
                'in_config': in_config
            }
        ).execute()

        self.assertTrue(
            isinstance(result, expectation_class)
        )
