import datetime
import os
import pytz

from django.conf import settings
from django.core.management import BaseCommand

from projects.models.pipeline import Pipeline


class Command(BaseCommand):
    help = """
        Cleanup old results
    """

    def handle(self, *args, **options):
        now = datetime.datetime.utcnow().replace(
            tzinfo=pytz.utc
        )

        ten_hours_ago = now - datetime.timedelta(hours=10)

        Pipeline.housekeeping(
            date_end=ten_hours_ago
        )
