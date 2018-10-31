import abc
import base64
import copy
import io

from django.core.files.uploadedfile import (
    InMemoryUploadedFile
)

from projects.models import *
from projects.serializers.pipeline import (
    PipelineResultFileSerializer
)


class Worker(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        processor = Processor()
        processor.id = self.id
        processor.name = self.name
        processor.image = self.image
        processor.description = self.description
        processor.schema = self.schema

        self.processor = processor
        if 'pipeline_result' in kwargs:
            result = kwargs['pipeline_result']
            self.pipeline = result.pipeline
            self.pipeline_result = result

        if 'pipeline_processor' in kwargs:
            self.set_pipeline_processor(
                kwargs['pipeline_processor']
            )

    def set_pipeline_processor(self, pipeline_processor: {}):
        self.pipeline_processor = PipelineProcessor(
            pipeline_processor
        )

    def check_input_data(self, data):
        return self.processor.check_input_data(data)

    def request_file(self):
        _file = PipelineResultFile()
        _file.prepare()
        return _file

    def prepare_output_data(self, data):
        if isinstance(data, PipelineResultFile):
            _file = copy.deepcopy(data)
            _file.post_process(self.pipeline_result)
            serializer = PipelineResultFileSerializer(
                instance=_file
            )
            data = serializer.data

        return data

    def prepare_input_data(self, data):
        """
            If Processor Input is a File this should convert
                Input Data into a `file descriptor` object
        """
        converted_data = copy.deepcopy(data)

        if self.processor.accepts_file():
            converted_data = self.pipeline_result.open_file(
                data
            )

        return converted_data

    @abc.abstractmethod
    def process(self, data=None):
        pass

    def execute(self, data=None):
        self.check_input_data(data)
        prepared_data = self.prepare_input_data(data)

        result = self.process(prepared_data)

        return self.prepare_output_data(result)
