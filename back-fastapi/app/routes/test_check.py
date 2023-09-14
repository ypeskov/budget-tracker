from pprint import pprint

from fastapi import APIRouter, Depends, Request
from app.dependencies.check_token import check_token


router = APIRouter(
    prefix='/test',
    dependencies=[Depends(check_token)]
)


@router.get('/check', name='test_check')
def test_check(request: Request):
    pprint(request.scope['state'].get('user'))
    return 'ololo'