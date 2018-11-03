from projects.workers.fetch_url import *
from projects.workers.get_object_property import *
from projects.workers.google_translate import *
from projects.workers.grayscale import *
from projects.workers.html_to_text import *
from projects.workers.markdown import *
from projects.workers.md5 import *
from projects.workers.random import *
from projects.workers.readability import *
from projects.workers.resize import *
from projects.workers.sentiment import *
from projects.workers.watermark import *

REGISTERED_WORKER_CLASSES = (
    FetchURL,
    GetObjectProperty,
    GoogleTranslate,
    Grayscale,
    HTMLToText,
    Markdown,
    Md5,
    Random,
    Readability,
    Resize,
    Sentiment,
    Watermark,
)


def import_registered_workers(apps, schema_editor):
    Processor = apps.get_model('projects', 'Processor')

    for registered_worker_class in REGISTERED_WORKER_CLASSES:
        registered_worker = registered_worker_class()
        if Processor.objects.filter(pk=registered_worker.id).exists():
            Processor.objects.filter(pk=registered_worker.id).update(**{
                'name': registered_worker.name,
                'image': registered_worker.image,
                'description': registered_worker.description,
                'schema': registered_worker.schema,
            })
        else:
            Processor.objects.create(**{
                'id': registered_worker.id,
                'name': registered_worker.name,
                'image': registered_worker.image,
                'description': registered_worker.description,
                'schema': registered_worker.schema,
            })
