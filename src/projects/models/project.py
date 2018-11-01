import uuid

from django.db import models

from core.models import WithDate


class Project(WithDate, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=666, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)

    def __str__(self):
        return str(self.id)

    def delete(self):
        """
        Remove all associated:
            * Pipeline
            * PipelineResult
            * PipelineResultFile
        """
        for pipeline in self.pipeline_set.all():
            pipeline.delete()

        super().delete()
