from jsonschema import validators


def extend_with_file(validator_class):
    def is_file(validator, value, instance, schema):
        pass

    return validators.extend(
        validator_class,
        {
            "type": is_file
        }
    )
