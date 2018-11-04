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
        today_midnight = datetime.datetime.combine(
            now,
            datetime.time.min
        ).replace(
            tzinfo=pytz.utc
        )

        yesterday_midnight = today_midnight - datetime.timedelta(days=1)

        Pipeline.housekeeping(
            date_start=yesterday_midnight,
            date_end=today_midnight
        )
