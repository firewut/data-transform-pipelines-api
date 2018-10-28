import jsonschema

from core.json_schema.file import *

PJSONSchema = extend_with_file(
    jsonschema.Draft4Validator
)
