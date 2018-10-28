from projects.workers.get_object_property import GetObjectProperty
from tests.base import BaseTestCase


class GetObjectPropertyTestCase(BaseTestCase):
    worker_class = GetObjectProperty

    @BaseTestCase.cases(
        (
            'plain',
            {'a': 'b'},
            {'property': 'a'},
            'b'
        ),
        (
            'nested',
            {'a': {'b': {'c': [1, 2, 3]}}},
            {'property': 'a.b.c'},
            [1, 2, 3]
        ),
        (
            'a_bit_nested',
            {'a': {'b': {'c': {'d': {'e': {'f': 'g'}}}}}},
            {'property': 'a.b.c.d.e'},
            {'f': 'g'}
        ),
    )
    def test_worker(self, obj, in_config, expectation):
        result = self.worker_class(
            pipeline_processor={
                'in_config': in_config
            }
        ).process(
            obj
        )
        self.assertEqual(result, expectation)
