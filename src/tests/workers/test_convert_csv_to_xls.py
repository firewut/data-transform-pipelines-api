import base64
import filecmp
import os

from django.conf import settings
import rest_framework

from projects.workers.convert_csv_to_xls import ConvertCSVtoXLS
from tests.base import BaseTestCase
from tests.workers.base import WorkerBaseTestCase


class ConvertCSVtoXLSTestCase(WorkerBaseTestCase):
    worker_class = ConvertCSVtoXLS

    csv_as_file = open(os.path.join(WorkerBaseTestCase.images_dir, "example.csv"), "rb")
    csv_as_data = base64.b64encode(
        open(os.path.join(WorkerBaseTestCase.images_dir, "example.csv"), "rb").read()
    ).decode()

    @BaseTestCase.cases(
        ("file_as_file", csv_as_file),
        ("file_as_data", csv_as_data),
    )
    def test_worker(self, value):
        result = self.worker_class(
            pipeline_result=self.pipeline_result,
            pipeline_processor={
                "id": "convert_csv_to_xls",
                "in_config": {"delimiter": ","},
            },
        ).execute(value)

        self.assertTrue(
            isinstance(result, rest_framework.utils.serializer_helpers.ReturnDict)
        )

        self.assertEqual(
            result["mimetype"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
