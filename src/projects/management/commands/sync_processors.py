import datetime
import os
import pytz

from django.conf import settings
from django.core.management import BaseCommand

from projects import workers


class Command(BaseCommand):
    help = """
        Import workers
    """

    def handle(self, *args, **options):
        workers.import_registered_workers()
