import uuid

from django.contrib.postgres.fields import (
    JSONField
)
from django.db import models

from projects.models.project import Project
from projects.models.processor import Processor
from core.models import WithDate


class Pipeline(WithDate, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=666, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    processors = JSONField(null=True, blank=True)

    def create_result(self):
        result_object = PipelineResult.objects.create(
            pipeline=self
        )

        return result_object

    def check_input_data(self, data):
        if self.processors and len(self.processors) > 0:
            first_processor = Processor.objects.get(pk=self.processors[0]['id'])
            first_processor.check_input_data(data)

        return


class PipelineResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, editable=False)
    ctime = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    error = JSONField(null=True, blank=True)
    result = JSONField(null=True, blank=True)
    is_finished = models.BooleanField(blank=True, default=False)
