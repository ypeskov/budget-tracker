from .available_settings import existing_settings
from .errors import (
    IncorrectSettingsTypeError,
    MissingSettingsKeyError,
    UnknownSettingsKeyError,
)


def validate_settings(template_json, input_json) -> None:
    if not isinstance(template_json, dict) or not isinstance(input_json, dict):
        raise IncorrectSettingsTypeError("template_json or input_json is not a dict")

    for key in input_json.keys():
        if key not in existing_settings:
            raise UnknownSettingsKeyError(key)

    for key in template_json.keys():
        if key not in input_json:
            raise MissingSettingsKeyError(key)

    for key, value in input_json.items():
        if isinstance(value, dict):
            validate_settings(template_json[key], value)
        else:
            # Skip type validation if template value is None (optional field)
            if template_json[key] is not None:
                if not isinstance(value, type(template_json[key])):
                    raise IncorrectSettingsTypeError(key)
            # If template is None but value is provided, accept string or None
            elif value is not None and not isinstance(value, str):
                raise IncorrectSettingsTypeError(key)
