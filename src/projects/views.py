from rest_framework import viewsets
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


class PipelineViewSet(viewsets.ModelViewSet):
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
    filter_fields = ('id', 'project', 'title', 'description')

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('-ctime')

    @action(methods=['POST', 'PUT'], detail=True)
    def process(self, request, pk=None, **kwargs):
        instance = self.get_object()

        response_data = {

        }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ProcessorsViewSet(viewsets.ModelViewSet):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    filter_fields = ('id', 'name', 'description')

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('pk')
