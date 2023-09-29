from fastapi import HTTPException, status


transaction_filters = (
    'page', 'per_page', 'is_income', 'categories', 'is_transfer', 'accounts', 'currencies', 'from_date', 'to_date')


def to_int(val: str) -> int | None:
    try:
        return int(val)
    except ValueError as e:
        return None


filter_functions = {
    'page': to_int,
    'per_page': to_int,
}


def prepare_filters(params: dict):
    for key, val in params.items():
        if key not in transaction_filters:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'Incorrect filter: {key}')
        if key in filter_functions:
            params[key] = filter_functions[key](val)
            if params[key] is None:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'Incorrect value [{val}] for filter [{key}]')
