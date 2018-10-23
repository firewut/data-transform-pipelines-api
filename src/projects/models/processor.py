from django.db import models
from django.contrib.postgres.fields import JSONField


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
