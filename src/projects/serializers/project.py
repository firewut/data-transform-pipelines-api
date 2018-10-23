from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from projects.models import Project
from projects.serializers.pipeline import *


class ProjectSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    pipelines = PipelineSerializer(
        source='pipeline_set',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Project
        depth = 1
        fields = (
            "id",
            "title",
            "description",
            "pipelines",
            "ctime",
            "mtime",
        )
