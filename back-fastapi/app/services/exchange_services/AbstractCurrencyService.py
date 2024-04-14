"""
AbstractCurrencyService.py - Abstract class for currency services.
"""
from abc import ABC, abstractmethod


class AbstractCurrencyService(ABC):
    def __init__(self):
        self.currency_beacon_api_url = None
        self.currency_beacon_api_key = None
        self.rates = None

    @abstractmethod
    def get_currency_rates(self, date: str) -> dict:
        pass
