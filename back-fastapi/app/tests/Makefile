# Path: app/tests/Makefile

default:
	pytest --disable-warnings

test:
	pytest -v --disable-warnings

test-auth:
	pytest -v --disable-warnings test_auth.py

test-accounts:
	pytest -v --disable-warnings test_accounts_api.py

cov-missing:
	#pytest --cov
	pytest --cov=app --cov-report=term-missing

cov-skip:
	pytest --cov-report term-missing:skip-covered --cov=app
