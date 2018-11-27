from datetime import datetime as _datetime
from datetime import date as _date
import csv
import codecs
import io

import xlsxwriter

from projects.workers.base import Worker


class ConvertCSVtoXLS(Worker):
    id = 'convert_csv_to_xls'
    name = 'convert_csv_to_xls'
    image = ''
    description = 'Convert CSV file to XLS Spreadsheet'
    schema = {
        "type": "object",
        "properties": {
            "in": {
                "type": [
                    "file",
                    "string",
                ],
                "description": "Original CSV to convert"
            },
            "in_config": {
                "type": "object",
                "properties": {
                    "delimiter": {
                        "type": "string",
                        "description": "values delimiter",
                        "default": ";",
                    },
                    "quotechar": {
                        "type": "string",
                        "description": "quotechar"
                    }
                }
            },
            "in_config_example": {
                "delimiter": ";",
            },
            "out": {
                "type": [
                    "file"
                ],
                "description": "XLS Spreadsheet"
            }
        },
        "required": [
            "in_config"
        ]
    }

    def process(self, data):
        in_config = self.pipeline_processor.in_config

        delimiter = in_config.get('delimiter', ';')
        quotechar = in_config.get('quotechar', None)

        if isinstance(data, str):
            data = io.BytesIO(data.encode('utf-8'))

        csv_reader = csv.reader(
            codecs.iterdecode(data, 'utf-8'),
            delimiter=delimiter,
            quotechar=quotechar,
        )

        _file = self.request_file()
        _file.mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        workbook = xlsxwriter.Workbook(_file.path)
        self.active_sheet = workbook.add_worksheet()
        self.active_sheet.max_column_widths = {}

        for row in csv_reader:
            self.write_row(row)

        workbook.close()

        return _file

    """
        Oficial Documentation & Stackoverflow :D
    """
    col = 0
    row = 0
    row_width_ratio = 1.05

    def write_row(self, *args, **kwargs):
        col = int(kwargs.get('col', self.col))
        row = int(kwargs.get('row', self.row))

        data = []
        for column_index, arg in enumerate(list(*args)):
            _arg = arg
            if isinstance(arg, str):
                _arg = "%s" % arg
            if isinstance(arg, (_date, _datetime)):
                _arg = ("%s" % arg.replace(tzinfo=None))[:19]

            data.append(_arg)

            # Max column width
            min_width = 0
            string_width = self.excel_string_width("%s" % _arg)
            if string_width > min_width:
                max_width = self.active_sheet.max_column_widths.get(
                    column_index,
                    min_width
                )
                if string_width > max_width:
                    self.active_sheet.max_column_widths[column_index] = string_width

        self.active_sheet.write_row(
            row, col, data
        )

        self.row += 1

    def excel_string_width(self, str):
        """
        Calculate the length of the string in Excel character units. This is only
        an example and won't give accurate results. It will need to be replaced
        by something more rigorous.

        """
        string_width = len(str)

        if string_width == 0:
            return 0
        else:
            return string_width * self.row_width_ratio
