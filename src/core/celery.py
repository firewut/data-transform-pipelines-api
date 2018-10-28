import os
import sys

from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Testing should not require External Dependency
if 'test' in sys.argv[1:]:
    from celery.contrib.testing import app as _app

    app = _app.TestApp(
        'core',
        config={
            'CELERY_TASK_EAGER_PROPAGATES': True,
            'CELERY_TASK_ALWAYS_EAGER': True,
        },
        set_as_current=True,
        enable_logging=True,
    )

app.autodiscover_tasks(
    [
        'projects',
        'projects.workers',
    ]
)

sys.path.insert(0, os.path.join(settings.BASE_DIR, 'apps'))
