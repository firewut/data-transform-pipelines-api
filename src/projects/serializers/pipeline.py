from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin


from projects.serializers.processor import *
from projects.models import (
    Pipeline,
    Processor,
)


class PipelineSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Pipeline
        fields = (
            "id",
            "description",
            "is_active",
            "processors",
            "project",
            "title",
            "ctime",
            "mtime",
        )
        read_only = (
            "id",
            "ctime",
            "mtime",
        )

    def _cleanup_processors(self, processors: []):
        cleaned_processors = []

        processor_allowed_properties = [
            'id',
            'in_config',
            'out_config'
        ]
        for processor in processors:
            cleaned_processor = {}
            for k, v in processor.items():
                if k in processor_allowed_properties:
                    cleaned_processor[k] = v
            cleaned_processors.append(cleaned_processor)

        return cleaned_processors

    def create(self, validated_data):
        processors = validated_data.pop('processors', None)
        if processors:
            validated_data['processors'] = self._cleanup_processors(
                processors
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        processors = validated_data.pop('processors', None)
        if processors:
            validated_data['processors'] = self._cleanup_processors(
                processors
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.processors:
            return representation

        instance_processors_ids = list()

        for _processor in instance.processors:
            instance_processors_ids.append(
                _processor.get('id')
            )

        template_processors = {}
        for processor in Processor.objects.filter_ids(instance_processors_ids):
            template_processors[processor.pk] = ProcessorSerializer(
                processor
            ).data

        for _processor in instance.processors:
            _processor.update({
                'template': template_processors.get(_processor.get('id'))
            })
        return representation

    def validate_processors(self, value):
        missing_processors = []
        processors_ids = set(
            Processor.objects.all().values_list('id', flat=True)
        )

        if isinstance(value, list):
            for _processor in value:
                if _processor['id'] not in processors_ids:
                    missing_processors.append(_processor['id'])

        if len(missing_processors) > 0:
            raise serializers.ValidationError(
                "Processors does not exist: {}".format(
                    missing_processors
                )
            )

        return value
