from django.db import models
from django.contrib.postgres.fields import JSONField
import jsonschema

from core import json_schema


class ProcessorManager(models.Manager):
    def filter_ids(self, id_list: []):
        """
            No Trust in Humanity
        """
        if not id_list:
            return self

        id_set = set(filter(None, id_list))
        return self.filter(id__in=id_set)


class Processor(models.Model):
    id = models.CharField(max_length=666, primary_key=True, editable=False)
    name = models.CharField(max_length=666, null=False, blank=False)
    image = models.TextField(
        null=True,
        default=None,
        blank=True
    )
    description = models.TextField(blank=True, null=True)
    schema = JSONField()

    objects = ProcessorManager()

    def __str__(self):
        return self.id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Beware - Extended JSONSchema used here
        self.jsonschema = json_schema.PJSONSchema

    def _get_type(self, direction: str = 'in'):
        _type = self.schema['properties'][direction]['type']
        if not isinstance(_type, list):
            _type = [_type, ]

        return _type

    def _get_out_type(self):
        return self._get_type('out')

    def _get_in_type(self):
        return self._get_type('in')

    def requires_input(self):
        in_type = self._get_in_type()
        if not in_type or \
                len(in_type) == 0 or \
                in_type == ['null']:
            return False

        return True

    def output_is_file(self):
        return 'file' in self._get_out_type()

    def input_is_file(self):
        return 'file' in self._get_in_type()

    def can_send_result(self, processor):
        out_type = self._get_out_type()
        in_type = processor._get_in_type()

        out_types = set(out_type)
        in_types = set(in_type)

        out_types.discard('null')
        in_types.discard('null')

        if len(in_types) == 0:
            return True

        intersection = out_types.intersection(in_types)

        return len(intersection) > 0

    def get_in_config_schema(self):
        return self.schema['properties'].get('in_config')

    def check_in_config(self, pipeline_processor):
        in_config_schema = self.get_in_config_schema()

        if pipeline_processor is None:
            raise jsonschema.exceptions.ValidationError(
                "Pipeline Processor is Required"
            )

        if isinstance(in_config_schema, dict):
            in_config = pipeline_processor.get('in_config', None)
            if in_config:
                self.jsonschema(in_config_schema).validate(in_config)
            else:
                raise jsonschema.exceptions.ValidationError(
                    "'in_config' is required"
                )

        return

    def check_input_data(self, data):
        in_schema = self.schema['properties'].get('in')

        if in_schema:
            self.jsonschema(in_schema).validate(data)

        return


class PipelineProcessor(object):
    id = None
    in_config = {}
    out_config = {}

    def __init__(self, data: {}):
        self.id = data.get('id')
        self.in_config = data.get('in_config', {})
        self.out_config = data.get('out_config', {})
