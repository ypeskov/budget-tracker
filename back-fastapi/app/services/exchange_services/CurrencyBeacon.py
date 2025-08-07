from requests import request

from app.config import Settings
from app.logger_config import logger
from app.services.exchange_services.AbstractCurrencyService import AbstractCurrencyService
from app.services.exchange_services.exceptions import ErrorFetchingData

s = Settings()

API_URL = s.CURRENCYBEACON_API_URL
API_KEY = s.CURRENCYBEACON_API_KEY
API_VERSION = s.CURRENCYBEACON_API_VERSION
SERVICE_NAME = 'CurrencyBeacon'


class CurrencyBeaconService(AbstractCurrencyService):
    def __init__(self):
        super().__init__()
        self.api_url = API_URL
        self.api_key = API_KEY
        self.api_version = API_VERSION

    def make_request(self, method: str, **kwargs) -> dict:
        params = '&'.join([f'{key}={value}' for key, value in kwargs.items()])
        url = f'{self.api_url}/{self.api_version}/{method}?api_key={self.api_key}&{params}'
        response = request('GET', url)
        if response.status_code != 200:
            logger.error(f'Error while fetching data: {response.text}, status code: {response.status_code}')
            raise ErrorFetchingData('Error while fetching data')
        return response.json()

    def get_currency_rates(self, when: str) -> dict:
        rates_data: dict = self.make_request('historical', date=when)
        return {
            'rates': rates_data['rates'],
            'actual_date': rates_data['date'],
            'base_currency_code': rates_data['base'],
            'service_name': SERVICE_NAME,
        }
