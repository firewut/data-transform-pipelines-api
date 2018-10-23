from django.db import models


class WithDate(models.Model):
    ctime = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    mtime = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract = True
