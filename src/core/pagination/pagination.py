from rest_framework import pagination
from rest_framework.response import Response

from django.conf import settings


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                },
                'count': self.page.paginator.count,
            },
            'results': data
        })
