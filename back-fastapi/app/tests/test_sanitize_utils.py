import pytest
from fastapi import status, HTTPException

from app.utils.sanitize_transaction_filters import prepare_filters, to_int, to_bool, to_int_list, to_str_list

import icecream
from icecream import ic

icecream.install()


def test_prepare_filter():
    param_str = 'page=1&per_page=10&types=expense,income&currencies=1,2,3&categories=1,2,3&accounts=1,2,3'
    params = dict(item.split('=') for item in param_str.split('&'))
    prepare_filters(params)
    assert params['page'] == 1
    assert params['per_page'] == 10
    assert params['types'] == ['expense', 'income']
    assert params['currencies'] == [1, 2, 3]
    assert params['categories'] == [1, 2, 3]
    assert params['accounts'] == [1, 2, 3]


def test_incorrect_prepare_filter():
    param_str = 'page=1&per_page=10&types=expense,income&currencies=1,2,3&categories=1,2,3&accounts=1,2,3&abc=123'
    params = dict(item.split('=') for item in param_str.split('&'))
    with pytest.raises(HTTPException) as ex:
        prepare_filters(params)
    assert ex.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert ex.value.detail == 'Incorrect filter: abc'


def test_incorrect_values_filter():
    param_str = 'page=abc&types=expense,income&currencies=a,b,g&categories=1,2,3&accounts=1,2,3&abc=123'
    params = dict(item.split('=') for item in param_str.split('&'))
    with pytest.raises(HTTPException) as ex:
        prepare_filters(params)
    assert ex.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert ex.value.detail == 'Incorrect value [abc] for filter [page]'

    incorrect_val = 'a,b,g'
    param_str = f'currencies={incorrect_val}'
    params = dict(item.split('=') for item in param_str.split('&'))
    with pytest.raises(HTTPException) as ex:
        prepare_filters(params)
    assert ex.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert params['currencies'] is None


def test_incorrect_to_int():
    processed_val = to_int('abc')
    assert processed_val is None

    processed_val = to_int('123')
    assert processed_val == 123

    processed_val = to_int('123.45')
    assert processed_val is None

    processed_val = to_int('123,45')
    assert processed_val is None


def test_incorrect_to_bool():
    processed_val = to_bool('abc')
    assert processed_val is True

    processed_val = to_bool('123')
    assert processed_val is True

    processed_val = to_bool('123.45')
    assert processed_val is True

    processed_val = to_bool('123,45')
    assert processed_val is True

    processed_val = to_bool('')
    assert processed_val is False

    processed_val = to_bool('0')
    assert processed_val is False

    processed_val = to_bool('false')
    assert processed_val is False

    processed_val = to_bool('False')
    assert processed_val is False

    processed_val = to_bool(None)  # type: ignore
    assert processed_val is False


def test_incorrect_to_int_list():
    processed_val = to_int_list('abc')
    assert processed_val is None

    processed_val = to_int_list('123')
    assert processed_val == [123]

    processed_val = to_int_list('123.45')
    assert processed_val is None

    processed_val = to_int_list('123,45')
    assert processed_val == [123, 45]

    processed_val = to_int_list('123, 45')
    assert processed_val == [123, 45]

    processed_val = to_int_list('123, 45, 67')
    assert processed_val == [123, 45, 67]


def test_incorrect_to_str_list():
    processed_val = to_str_list('abc')
    assert processed_val == ['abc']

    processed_val = to_str_list('abc, der')
    assert processed_val == ['abc', 'der']

    processed_val = to_str_list('123')
    assert processed_val == ['123']

    processed_val = to_str_list('123.45')
    assert processed_val == ['123.45']

    processed_val = to_str_list('123,45')
    assert processed_val == ['123', '45']

    processed_val = to_str_list('123, 45')
    assert processed_val == ['123', '45']

    processed_val = to_str_list('123, 45, 67')
    assert processed_val == ['123', '45', '67']

    processed_val = to_str_list('123,45,67')
    assert processed_val == ['123', '45', '67']
