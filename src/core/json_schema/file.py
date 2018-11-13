import io

from django.core.files.uploadedfile import (
    InMemoryUploadedFile
)
import jsonschema

FILE_TYPE_SCHEMA = {
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string'
        },
    },
    'additionalProperties': True
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
        )
    )


def file_checker(checker, instance):
    if not isinstance(
        instance, (
            # Base64
            str,
            # internally provided
            io.BytesIO,
            io.BufferedReader,
            # file upload
            InMemoryUploadedFile,
            # JSON in case if file uploaded recently
            dict,
        )
    ):
        return False

    if isinstance(instance, dict):
        try:
            jsonschema.validate(instance, FILE_TYPE_SCHEMA)
        except jsonschema.exceptions.ValidationError:
            return False

    return True
