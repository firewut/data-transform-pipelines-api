import abc

from projects.models import *


class Worker(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        processor = Processor()
        processor.id = self.id
        processor.name = self.name
        processor.image = self.image
        processor.description = self.description
        processor.schema = self.schema

        if 'pipeline_processor' in kwargs:
            self.set_pipeline_processor(
                kwargs['pipeline_processor']
            )

        self.processor = processor

    @abc.abstractmethod
    def process(self, data=None):
        pass

    def set_pipeline_processor(self, pipeline_processor: {}):
        self.pipeline_processor = PipelineProcessor(
            pipeline_processor
        )
