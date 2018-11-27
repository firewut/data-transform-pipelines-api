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
    id = None
    name = ""
    description = ""
    image = ""
    schema = {}
    ui_schema = None
    input_is_file = False

    # helpers
    raw_input_data = None

    def __init__(self, *args, **kwargs):
        processor = Processor()
        processor.id = self.id
        processor.name = self.name
        processor.image = self.image
        processor.description = self.description
        processor.schema = self.schema
        processor.ui_schema = self.ui_schema

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

    def open_file(self, value):
        _file, _ = self.pipeline_result.open_file(
            value
        )
        return _file

    def request_file(self):
        _file = PipelineResultFile()
        _file.prepare()

        return _file

    def prepare_output_data(self, data):
        if self.processor.output_is_file():
            if isinstance(data, PipelineResultFile):
                _file = copy.deepcopy(data)
                _file.post_process(self.pipeline_result)
                serializer = PipelineResultFileSerializer(
                    instance=_file
                )
                data = serializer.data
            else:
                if isinstance(data, io.BufferedReader):
                    # Reuse previous step file
                    data = self.raw_input_data

        return data

    def discard_files(self, data):
        if self.input_is_file:
            if isinstance(data, dict):
                PipelineResultFile.remove_by_id(data.get('id'))

    def prepare_input_data(self, data):
        """
            If Processor Input is a File this should convert
                Input Data into a `file descriptor` object
        """

        try:
            self.raw_input_data = copy.deepcopy(data)
            converted_data = copy.deepcopy(data)
        except TypeError:
            self.raw_input_data = data
            converted_data = data

        if self.processor.input_is_file() and self.pipeline.check_is_internal_file(data):
            converted_data, is_opened = self.pipeline_result.open_file(
                data,
                self.processor.input_is_file_only()
            )
            self.input_is_file = is_opened

        return converted_data

    @abc.abstractmethod
    def process(self, data=None):
        pass

    def execute(self, data=None):
        self.check_input_data(data)
        prepared_data = self.prepare_input_data(data)

        result = self.process(prepared_data)
        return self.prepare_output_data(result)
