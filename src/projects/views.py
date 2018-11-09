import json

from rest_framework import (
    viewsets,
    status,
    generics,
    mixins,
    views,
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


class PipelineResultViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = PipelineResult.objects.all()
    serializer_class = PipelineResultSerializer


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

            Accepts `application/json` or `multipart/form-data` Content-Types

            `processors` are Optional for preview:
                application/json - JSON Object
                multipart/form-data - JSON Object as a String

            If `application/json` - root property should be named `data`
            If `multipart/form-data` - the field should be named `file`
        """
        instance = self.get_object()

        pipeline_processors = instance.processors

        if isinstance(request.data, type({})):
            if 'application/json' in request.content_type:
                pipeline_processors = request.data.get(
                    'processors',
                    pipeline_processors
                )
            elif 'multipart/form-data' in request.content_type:
                pipeline_processors = json.loads(
                    request.data.get('processors', '{}')
                ) or pipeline_processors

        #   TODO: Think about replacing this    #
        instance.processors = pipeline_processors
        if not instance.processors:
            return Response(
                {
                    "error": "No processors passed"
                },
                status=422,
            )
        #########################################

        pipeline_serializer = PipelineSerializer
        pipeline_serializer().check_processors(
            instance.processors
        )

        input_data = None

        if instance.requires_input_data():
            input_data = request.data
            if 'application/json' in request.content_type:
                input_data = request.data.get(
                    'data',
                )

            for k, v in request.FILES.items():
                if k.lower() == 'file':
                    input_data = v
                    break

            instance.check_input_data(input_data)

        pipeline_result = instance.create_result(
            input_data
        )

        serializer_class = PipelineResultSerializer
        response_data = serializer_class(
            pipeline_result
        ).data

        return Response(
            response_data,
            status=status.HTTP_202_ACCEPTED,
            headers={
                'Location': reverse(
                    'pipeline_result-detail',
                    args=(
                        response_data['id'],
                    ),
                    request=request,
                )
            }
        )


class ProcessorsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    filter_fields = ('id', 'name', 'description')

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('pk')
