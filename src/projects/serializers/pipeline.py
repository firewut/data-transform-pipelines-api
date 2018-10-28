from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from projects.serializers.processor import *
from projects.models import (
    Pipeline,
    PipelineResult,
    Processor,
)


class PipelineResultSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = PipelineResult
        fields = (
            'id',
            'pipeline',
            'ctime',
            'error',
            'result',
            'is_finished',
        )
        read_only = (
            'id',
            'pipeline',
            'ctime',
            'error',
            'result',
            'is_finished',
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

    def check_processors(self, processors: []):
        # Retrieve processors used in a Pipeline
        _processors = {}
        for processor in processors:
            if processor['id'] not in _processors.keys():
                _processors[processor['id']] = Processor.objects.get(pk=processor['id'])

        # Check Pipeline Data Flow
        for i in range(0, len(processors) - 1):
            current_processor = _processors[processors[i]['id']]
            next_processor = _processors[processors[i + 1]['id']]

            if not current_processor.can_send_result(next_processor):
                raise serializers.ValidationError(
                    "{}[{}] is incompatible with next processor {}".format(
                        current_processor.id, i, next_processor.id
                    )
                )

        # Check Processor in_config and out_config
        for i, processor in enumerate(processors):
            _processor = _processors[processor['id']]

            try:
                _processor.check_in_config(processor)
            except Exception as e:
                raise serializers.ValidationError(
                    "{}[{}] has invalid in_config".format(
                        _processor.id, i
                    )
                )

        return

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
            self.check_processors(validated_data['processors'])

        return super().create(validated_data)

    def update(self, instance, validated_data):
        processors = validated_data.pop('processors', None)
        if processors:
            validated_data['processors'] = self._cleanup_processors(
                processors
            )
            self.check_processors(validated_data['processors'])
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
