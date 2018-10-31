from jsonschema.validators import (
    Draft4Validator,
    extend,
)

from core.json_schema.file import *


PJSONSchema = extend(
    Draft4Validator,
    type_checker=Draft4Validator.TYPE_CHECKER.redefine(
        "file", file_checker,
    ),
)
