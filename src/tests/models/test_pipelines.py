from django.core.exceptions import ObjectDoesNotExist
import datetime
import pytz

from projects.models import *
from tests.base import BaseTestCase


class PipelinesTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            title=self.random_string(30),
            description=self.random_string(30),
        )
        self.pipeline = Pipeline.objects.create(
            project=self.project,
            title=self.random_string(30),
            description=self.random_string(30),
        )

    def test_pipeline_removal(self):
        # Create Result
        result = PipelineResult.objects.create(pipeline=self.pipeline)
        # Create a ResultFile
        result_file = PipelineResultFile()
        result_file.prepare()

        with open(result_file.path, "w") as fp:
            fp.write(self.random_string(30))

        result_file.post_process(result)

        result_file_path = result_file.path

        self.pipeline.delete()

        with self.assertRaises(ObjectDoesNotExist):
            PipelineResult.objects.get(pk=result.pk)

        with self.assertRaises(ObjectDoesNotExist):
            PipelineResultFile.objects.get(pk=result_file.pk)

        self.assertFalse(os.path.exists(result_file_path))

    def test_pipeline_remove_results_after_moment(self):
        moment_in_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        # Create Result
        result = PipelineResult.objects.create(pipeline=self.pipeline)
        # Create a ResultFile
        result_file = PipelineResultFile()
        result_file.prepare()

        with open(result_file.path, "w") as fp:
            fp.write(self.random_string(30))

        result_file.post_process(result)

        result_file_path = result_file.path

        self.pipeline.remove_results(date_start=moment_in_time)

        with self.assertRaises(ObjectDoesNotExist):
            PipelineResult.objects.get(pk=result.pk)

        with self.assertRaises(ObjectDoesNotExist):
            PipelineResultFile.objects.get(pk=result_file.pk)

        self.assertFalse(os.path.exists(result_file_path))

    def test_pipeline_remove_results_before_moment(self):
        # Create Result
        result = PipelineResult.objects.create(pipeline=self.pipeline)
        # Create a ResultFile
        result_file = PipelineResultFile()
        result_file.prepare()

        with open(result_file.path, "w") as fp:
            fp.write(self.random_string(30))

        result_file.post_process(result)

        result_file_path = result_file.path

        moment_in_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self.pipeline.remove_results(date_end=moment_in_time)

        with self.assertRaises(ObjectDoesNotExist):
            PipelineResult.objects.get(pk=result.pk)

        with self.assertRaises(ObjectDoesNotExist):
            PipelineResultFile.objects.get(pk=result_file.pk)

        self.assertFalse(os.path.exists(result_file_path))
