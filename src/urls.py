from django.urls import include, path

from rest_framework.documentation import include_docs_urls
from rest_framework.renderers import DocumentationRenderer
from rest_framework.routers import DefaultRouter

from projects.views import *


class DocumentationRenderer(DocumentationRenderer):
    languages = ["javascript", "python"]


API_TITLE = "Data Transform API"
API_DESCRIPTION = "Simple Pipeline Based"


router = DefaultRouter()
router.register(r"processors", ProcessorsViewSet, basename="processors")
router.register(r"projects", ProjectsViewSet, basename="projects")
router.register(r"pipelines", PipelineViewSet, basename="pipelines")
router.register(r"pipeline_result", PipelineResultViewSet, basename="pipeline_result")
router.register(r"files", PipelineResultFileViewSet, basename="files_x_accel_redirect")

urlpatterns = [
    path(settings.API_URL, include(router.urls)),
    path(
        "{}docs/".format(settings.API_URL),
        include_docs_urls(
            title=API_TITLE,
            description=API_DESCRIPTION,
            public=True,
            authentication_classes=[],
            permission_classes=[],
            renderer_classes=[DocumentationRenderer],
        ),
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
