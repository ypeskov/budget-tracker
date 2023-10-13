from fastapi import HTTPException, status


transaction_filters = (
    'page', 'per_page', 'types', 'categories', 'accounts', 'currencies', 'from_date', 'to_date')


def to_int(val: str) -> int | None:
    try:
        return int(val)
    except ValueError:
        return None


def to_bool(val: str) -> bool:
    false_values = ('', '0', 'false', 'False', None)
    return val not in false_values


def to_int_list(val: str) -> list | None:
    try:
        return [int(item) for item in map(str.strip, val.split(','))]
    except ValueError:
        return None


def to_str_list(val: str) -> list | None:
    return [transfer_type for transfer_type in map(str.strip, val.split(','))]


filter_functions = {
    'page': to_int,
    'per_page': to_int,
    'types': to_str_list,
    'currencies': to_int_list,
    'categories': to_int_list,
    'accounts': to_int_list,
}


def prepare_filters(params: dict):
    for key, val in params.items():
        if key not in transaction_filters:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'Incorrect filter: {key}')
        if key in filter_functions:
            params[key] = filter_functions[key](val)
            if params[key] is None:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'Incorrect value [{val}] for filter [{key}]')
