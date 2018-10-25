from projects.models import *

from celery import shared_task


@shared_task
def process(
    pipeline_result_id: str,
    pipeline_processors: [],
    data=None,
):
    pass
