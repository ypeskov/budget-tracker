from icecream import ic
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.Currency import Currency


def load_default_currencies(db: Session | None = None):
    if db is None:
        db = next(get_db())  # pragma: no cover

    default_values = [
        Currency(id=1, code='USD', name='United States Dollar'),
        Currency(id=2, code='UAH', name='Ukrainian Hryvna'),
        Currency(id=3, code='EUR', name='Euro'),
        Currency(id=4, code='BGN', name='Bulgarian Lev'),
        Currency(id=5, code='AUD', name='Australian Dollar'),
        Currency(id=6, code='BRL', name='Brazilian Real'),
        Currency(id=7, code='CAD', name='Canadian Dollar'),
        Currency(id=8, code='CHF', name='Swiss Franc'),
        Currency(id=9, code='CNY', name='Chinese Yuan'),
        Currency(id=10, code='CZK', name='Czech Koruna'),
        Currency(id=11, code='DKK', name='Danish Krone'),
        Currency(id=12, code='GBP', name='British Pound'),
        Currency(id=13, code='HKD', name='Hong Kong Dollar'),
        Currency(id=14, code='HRK', name='Croatian Kuna'),
        Currency(id=15, code='HUF', name='Hungarian Forint'),
        Currency(id=16, code='IDR', name='Indonesian Rupiah'),
        Currency(id=17, code='ILS', name='Israeli New Shekel'),
        Currency(id=18, code='INR', name='Indian Rupee'),
        Currency(id=19, code='ISK', name='Icelandic Krona'),
        Currency(id=20, code='JPY', name='Japanese Yen'),
        Currency(id=21, code='KRW', name='South Korean Won'),
        Currency(id=22, code='MXN', name='Mexican Peso'),
        Currency(id=23, code='MYR', name='Malaysian Ringgit'),
        Currency(id=24, code='NOK', name='Norwegian Krone'),
        Currency(id=25, code='NZD', name='New Zealand Dollar'),
        Currency(id=26, code='PHP', name='Philippine Peso'),
        Currency(id=27, code='PLN', name='Polish Zloty'),
        Currency(id=28, code='RON', name='Romanian Leu'),
        Currency(id=29, code='RUB', name='Russian Ruble'),
        Currency(id=30, code='SEK', name='Swedish Krona'),
        Currency(id=31, code='SGD', name='Singapore Dollar'),
        Currency(id=32, code='THB', name='Thai Baht'),
        Currency(id=33, code='TRY', name='Turkish Lira'),
        Currency(id=34, code='ZAR', name='South African Rand'),
    ]

    for currency_item in default_values:
        existing = db.query(Currency).filter_by(id=currency_item.id).first()
        if not existing:
            # print(f'Adding currency: {currency_item}')
            new_currency = Currency(
                id=currency_item.id, code=currency_item.code, name=currency_item.name
            )
            db.add(new_currency)

    try:
        db.commit()
        print(f'Default currencies are loaded in the table [{Currency.__tablename__}]')
    except IntegrityError as e:
        db.rollback()
        ic(e.args)
        print(f"Some currencies might already exist. No changes made.")
    except Exception as e:  # pragma: no cover
        ic(e.args)


if __name__ == '__main__':  # pragma: no cover
    load_default_currencies()
