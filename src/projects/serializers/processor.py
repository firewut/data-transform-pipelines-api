from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from projects.models.processor import Processor


class ProcessorSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Processor
        fields = (
            '__all__'
        )
