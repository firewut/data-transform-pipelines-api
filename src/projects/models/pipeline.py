import uuid

from django.contrib.postgres.fields import (
    JSONField
)
from django.db import models

from projects.models.project import Project
from core.models import WithDate


class Pipeline(WithDate, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=666, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    processors = JSONField(null=True, blank=True)
