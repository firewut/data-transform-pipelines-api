from rest_framework import viewsets
from rest_framework.response import Response

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


class ProcessorsViewSet(viewsets.ModelViewSet):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    filter_fields = ('id', 'name', 'description')

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('pk')
