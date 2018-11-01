from projects.models import *
from tests.base import BaseTestCase


class WorkerBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.project = Project.objects.create(
            title=self.random_string(30)
        )
        self.pipeline = Pipeline.objects.create(
            title=self.random_string(),
            project=self.project,
        )
        self.pipeline_result = PipelineResult.objects.create(
            pipeline=self.pipeline,
        )

    def tearDown(self):
        self.project.delete()
        self.pipeline.delete()
        self.pipeline_result.delete()

        self.assertIsNone(self.project.pk)
        self.assertIsNone(self.pipeline.pk)
        self.assertIsNone(self.pipeline_result.pk)

        super().tearDown()
