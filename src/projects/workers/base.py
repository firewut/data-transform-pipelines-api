import abc
import base64
import io

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
        return PipelineResultFile()

    def prepare_output_data(self, data):
        if isintance(data, PipelineResultFile):
            _file = data
            _file.post_process(self.pipeline_result)
            data = PipelineResultFileSerializer(data=_file).data

        return data

    def prepare_input_data(self, data):
        """
            If Processor Input is a File this should convert
                Input Data into a `file descriptor` object
        """
        converted_data = data

        in_type = self.processor.schema['properties']['in']['type']
        if not isinstance(in_type, list):
            in_type = [in_type, ]

        in_types = set(in_type)
        if 'file' in in_types:
            # base64 encoded data
            if isinstance(data, str):
                converted_data = io.BytesIO(
                    base64.b64decode(data)
                )

            # already prepared
            if isinstance(data, io.BufferedReader):
                pass

            # API File Interface
            if isinstance(data, dict):
                if 'id' in data:
                    try:
                        result_file = PipelineResultFile.objects.get(
                            pk=data['id']
                        )
                        converted_data = open(
                            result_file.path, 'rb'
                        )
                    except Exception as e:
                        pass

        return converted_data

    @abc.abstractmethod
    def process(self, data=None):
        pass

    def execute(self, data=None):
        self.check_input_data(data)
        prepared_data = self.prepare_input_data(data)

        return self.process(prepared_data)
