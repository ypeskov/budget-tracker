# Path: app/tests/Makefile

default:
	pytest -s --disable-warnings

test:
	pytest -vs --disable-warnings

test-auth:
	pytest -vs --disable-warnings test_auth.py

test-accounts:
	pytest -vs --disable-warnings test_accounts_api.py

cov-missing:
	#pytest --cov
	pytest --cov=app --cov-report=term-missing

cov:
	pytest --cov-report term-missing:skip-covered --cov=app
