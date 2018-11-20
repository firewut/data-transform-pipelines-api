from urllib import request
import base64
import hashlib
import io
import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import (
    InMemoryUploadedFile
)
from django.core.validators import URLValidator
from django.contrib.postgres.fields import (
    JSONField
)
from django.db import models
from requests.exceptions import HTTPError
import celery
import magic
import requests

from core.json_schema.file import check_is_internal_file
from core.models import WithDate
from core.utils import random_uuid4
from projects.models.project import Project
from projects.models.processor import Processor


class Pipeline(WithDate, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=666, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    processors = JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def check_is_internal_file(self, data):
        if not check_is_internal_file(data):
            _, is_opened = PipelineResult.open_file(data)
            if is_opened:
                return True
        else:
            return True
        return False

    def create_result(self, data):
        result_object = PipelineResult.objects.create(
            pipeline=self
        )

        if self.accepts_file() and self.check_is_internal_file(data):
            input_file = result_object.save_file(data)
            data = {
                'id': input_file.pk,
            }

        # Generate a task to queue processing
        celery.current_app.send_task(
            'projects.tasks.process_pipeline',
            kwargs={
                'result_id': result_object.pk,
                'processors': self.processors,
                'data': data,
                'error': None,
            }
        )

        return result_object

    def requires_input_data(self):
        first_processor = self.get_first_processor()
        if first_processor:
            return first_processor.requires_input()

        return False

    def get_first_processor(self):
        first_processor = None
        if self.processors and len(self.processors) > 0:
            first_processor = Processor.objects.get(pk=self.processors[0]['id'])

        return first_processor

    def check_input_data(self, data):
        first_processor = self.get_first_processor()
        if first_processor:
            first_processor.check_input_data(data)

        return

    def accepts_file(self):
        """
            Helper for first processor input data type
        """
        first_processor = self.get_first_processor()
        if first_processor:
            return first_processor.input_is_file()

        return False

    @classmethod
    def housekeeping(cls, conditions: models.Q = None, date_start=None, date_end=None):
        """
            Mass Results cleanup
        """
        if not conditions:
            conditions = models.Q()

        if date_start:
            conditions &= models.Q(ctime__gte=date_start)

        if date_end:
            conditions &= models.Q(ctime__lte=date_end)

        results = PipelineResult.objects.filter(conditions)
        for result in results:
            result.delete()

    def remove_results(self, date_start=None, date_end=None):
        """
            Remove all Results and Associated Files
                older than some moment
        """
        conditions = models.Q(pipeline=self)
        Pipeline.housekeeping(
            conditions=models.Q(pipeline=self),
            date_start=date_start,
            date_end=date_end
        )

    def delete(self):
        """
            Remove all Results and Associated Files
        """
        self.remove_results()

        super().delete()


class PipelineResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, editable=False)
    ctime = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    error = JSONField(null=True, blank=True)
    result = JSONField(null=True, blank=True)
    is_finished = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return str(self.id)

    def delete_unused_files(self):
        if not self.result:
            return

        for _file in PipelineResultFile.objects.filter(
            pipeline_result=self
        ):
            if self.result.get('id') != str(_file.id):
                _file.delete()

    def delete(self):
        for _file in PipelineResultFile.objects.filter(
            pipeline_result=self
        ):
            _file.delete()

        super().delete()

    @classmethod
    def open_file(cls, data, raise_exception=False):
        input_file = None
        is_opened = False

        if check_is_internal_file(data):
            input_file = data
            is_opened = True
        elif isinstance(data, str):
            url_validator = URLValidator()
            # It may be a valid URL or base64 encoded string
            try:
                try:
                    url_validator(data)
                    response = requests.get(data)
                    response.raise_for_status()
                    input_file = io.BytesIO(response.content)
                    is_opened = True
                except ValidationError:
                    input_file = io.BytesIO(
                        base64.b64decode(data)
                    )
                    is_opened = True
            except Exception as e:
                if raise_exception:
                    raise e
                input_file = data

        elif isinstance(data, dict):
            if 'id' in data:
                try:
                    _file = PipelineResultFile.objects.get(
                        pk=data['id']
                    )
                    input_file = _file.open()
                    is_opened = True
                except Exception as e:
                    if raise_exception:
                        raise e
                    input_file = data

        return input_file, is_opened

    def save_file(self, data):
        input_file = PipelineResultFile()
        input_file.prepare()

        converted_data, is_opened = PipelineResult.open_file(data)

        if self.pipeline.check_is_internal_file(data) and is_opened:
            default_storage.save(
                input_file.path,
                ContentFile(converted_data.read())
            )
            input_file.post_process(self)

        return input_file


class PipelineResultFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path = models.CharField(max_length=666, null=False, blank=False)
    pipeline_result = models.ForeignKey(PipelineResult, on_delete=models.CASCADE, editable=False)
    md5_hash = models.CharField(max_length=64, editable=False)
    size = models.BigIntegerField(default=0)
    mimetype = models.CharField(max_length=666, null=True, blank=True)
    ctime = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    _saved = False

    def __str__(self):
        return str(self.id)

    @classmethod
    def remove_by_id(cls, file_id: dict = None):
        if not file_id:
            return

        file_path = os.path.join(
            settings.MEDIA_ROOT,
            file_id
        )
        if os.path.exists(file_path):
            os.remove(file_path)

    def delete(self):
        if os.path.exists(self.path):
            os.remove(self.path)

        super().delete()

    def prepare(self, *args, **kwargs):
        self.id = random_uuid4()
        self.path = os.path.join(
            settings.MEDIA_ROOT,
            self.id
        )

        if os.path.isfile(self.path):
            self._saved = True

    def post_process(self, pipeline_result):
        hash_md5 = hashlib.md5()

        if not self._saved:
            with open(self.path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)

                f.seek(0, os.SEEK_END)
                self.size = f.tell()

            try:
                mime = magic.Magic(mime=True)
                self.mimetype = mime.from_file(self.path)
            except Exception as e:
                pass

            self.md5_hash = hash_md5.hexdigest()
            self.pipeline_result = pipeline_result
            self.save()
            self._saved = True

    def open(self):
        return open(self.path, 'rb')
