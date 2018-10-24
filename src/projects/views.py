from rest_framework import (
    viewsets,
    status,
)
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action

from projects.models import *
from projects.serializers import *


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_fields = ('id', 'title', 'description')

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('-ctime')


class PipelineResultViewSet(viewsets.ModelViewSet):
    queryset = PipelineResult.objects.all()
    serializer_class = PipelineResultSerializer
    filter_fields = ('id', 'pipeline', 'is_finished')

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('-ctime')


class PipelineViewSet(viewsets.ModelViewSet):
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
    filter_fields = ('id', 'project', 'title', 'description')

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('-ctime')

    @action(methods=['POST', 'PUT'], detail=True)
    def process(self, request, pk=None, **kwargs):
        """
            Queues a Pipeline Processing. 
            In case of Success you'll get HTTP 202 Status Code.
            Check *Location* Response Header to retrieve Pipeline Result.
        """
        instance = self.get_object()

        serializer_class = PipelineResultSerializer

        instance.check_input_data(request.data)
        pipeline_result = instance.create_result()

        response_data = serializer_class(pipeline_result).data

        return Response(
            response_data,
            status=status.HTTP_202_ACCEPTED,
            headers={
                'Location': reverse(
                    'pipeline_results-detail',
                    args=(
                        response_data['id'],
                    ),
                    request=request,
                )
            }
        )

    @action(methods=['GET'], detail=True)
    def results(self, request, pk=None, **kwargs):
        instance = self.get_objects()

        return Response(
            {},
            status=status.HTTP_201_CREATED,
            headers={}
        )


class ProcessorsViewSet(viewsets.ModelViewSet):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    filter_fields = ('id', 'name', 'description')

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('pk')
