from jsonschema import validators
from jsonschema.validators import _LATEST_VERSION as LATEST_VALIDATOR


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema and isinstance(instance, dict):
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties" : set_defaults},
    )


ExtendedDefaultValidator = extend_with_default(LATEST_VALIDATOR)
