test_account_types = [
    {
        'id': 1,
        'name': 'cash',
        'is_credit': False
    },
    {
        'id': 2,
        'name': 'regular_bank',
        'is_credit': False
    },
    {
        'id': 3,
        'name': 'debit_card',
        'is_credit': False
    },
    {
        'id': 4,
        'name': 'credit_card',
        'is_credit': True
    },
    {
        'id': 5,
        'name': 'loan',
        'is_credit': True
    },
]

test_accounts = [
    {
        'id': 1,
        "name": "Test Account 1 (USD)",
        "currency_id": 1,
        "account_type_id": 2,
        "balance": 500_000
    },
    {
        'id': 2,
        "name": "Test Account 2 (USD)",
        "currency_id": 1,
        "account_type_id": 2,
        "balance": 30_000
    },
    {
        'id': 3,
        "name": "Test Account 1 (UAH)",
        "currency_id": 2,
        "account_type_id": 2,
        "balance": 1_000_000
    },
    {
        'id': 4,
        "name": "Test Account 2 (UAH)",
        "currency_id": 2,
        "account_type_id": 2,
        "balance": 20_000
    },
    {
        'id': 5,
        "name": "Test Account 1 (EUR)",
        "currency_id": 3,
        "account_type_id": 2,
        "balance": 250_000
    },
    {
        'id': 6,
        "name": "Test Account 2 (EUR)",
        "currency_id": 3,
        "account_type_id": 2,
        "balance": 350_000
    },
    {
        'id': 7,
        "name": "Test Account 1 (BGN)",
        "currency_id": 4,
        "account_type_id": 1,
        "balance": 0
    },
    {
        'id': 8,
        "name": "Test Account 2 (BGN)",
        "currency_id": 4,
        "account_type_id": 2,
        "balance": 25_000
    },
]
