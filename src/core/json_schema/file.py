import io
import re

from django.core.files.uploadedfile import InMemoryUploadedFile
import jsonschema

FILE_TYPE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
    },
    "additionalProperties": True,
}


def check_is_internal_file(data):
    """
    Use this only if you know why.
    Check Pipeline method with same name
    """
    return isinstance(
        data,
        (
            io.BytesIO,
            io.BufferedReader,
            InMemoryUploadedFile,
        ),
    )


def is_base64(value: str):
    match = re.compile(
        "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
    ).match(value)
    if match:
        return match.pos == 0
    return False


def file_checker(checker, instance):
    if isinstance(instance, str):
        return is_base64(instance)

    if not isinstance(
        instance,
        (
            # internally provided
            io.BytesIO,
            io.BufferedReader,
            # file upload
            InMemoryUploadedFile,
            # JSON in case if file uploaded recently
            dict,
        ),
    ):
        return False

    if isinstance(instance, dict):
        try:
            jsonschema.validate(instance, FILE_TYPE_SCHEMA)
        except jsonschema.exceptions.ValidationError:
            return False

    return True
