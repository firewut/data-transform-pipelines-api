from celery import shared_task
import celery
import jsonschema

from projects.models import *
from projects.workers import *


@shared_task
def process_pipeline(
    result_id: str,
    processors: [],
    data=None,
    error=None,
):
    if not processors or \
            len(processors) == 0 \
            or error:

        result = PipelineResult.objects.get(
            pk=result_id,
        )
        result.result = data
        result.error = error
        result.is_finished = True
        result.save()
        return

    pipeline_processor = processors.pop(0)
    for REGISTERED_WORKER_CLASS in REGISTERED_WORKER_CLASSES:
        if pipeline_processor.get('id') == REGISTERED_WORKER_CLASS.id:
            worker_instance = REGISTERED_WORKER_CLASS(
                pipeline_processor=pipeline_processor
            )

            error = None
            result = data
            try:
                result = worker_instance.process(
                    data
                )
            except jsonschema.exceptions.ValidationError as e:
                error = str(e)
            except Exception as e:
                error = "{}: Internal Processing Error".format(
                    worker_instance.id,
                )

            celery.current_app.send_task(
                'projects.tasks.process_pipeline',
                kwargs={
                    'result_id': result_id,
                    'processors': processors,
                    'data': result,
                    'error': error,
                }
            )
            break
