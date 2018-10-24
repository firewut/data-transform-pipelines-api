from django.db import models
from django.contrib.postgres.fields import JSONField

import jsonschema


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

    def can_send_result(self, processor):
        out_type = self.schema['properties']['out']['type']
        in_type = processor.schema['properties']['in']['type']

        if not isinstance(out_type, list):
            out_type = [out_type, ]

        if not isinstance(in_type, list):
            in_type = [in_type, ]

        out_types = set(out_type)
        in_types = set(in_type)

        out_types.discard('null')
        in_types.discard('null')

        if len(in_types) == 0:
            return True

        intersection = out_types.intersection(in_types)

        return len(intersection) > 0

    def check_in_config(self, pipeline_processor):
        in_config_schema = self.schema['properties'].get('in_config')

        if isinstance(in_config_schema, dict):
            in_config = pipeline_processor.get('in_config', None)
            if in_config:
                jsonschema.validate(in_config, in_config_schema)

        return

    def check_input_data(self, data):
        in_schema = self.schema['properties'].get('in')
        if in_schema:
            jsonschema.validate(data, in_schema)

        return
