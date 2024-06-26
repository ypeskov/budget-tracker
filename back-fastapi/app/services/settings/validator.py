from icecream import ic

from .errors import UnknownSettingsKeyError, MissingSettingsKeyError, IncorrectSettingsTypeError

ic.configureOutput(includeContext=True)


def validate_settings(template_json, input_json):

    if not isinstance(template_json, dict) or not isinstance(input_json, dict):
        return False

    for key in input_json.keys():
        if key not in template_json:
            raise UnknownSettingsKeyError(key)

    for key in template_json.keys():
        if key not in input_json:
            raise MissingSettingsKeyError(key)

    for key, value in input_json.items():
        if isinstance(value, dict):
            validate_settings(template_json[key], value)
        else:
            if type(value) != type(template_json[key]):
                raise IncorrectSettingsTypeError(key)

    return True
