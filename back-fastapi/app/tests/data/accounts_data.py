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
        "currencyId": 1,
        "accountTypeId": 2,
        'initial_balance': 500_000,
        "balance": 500_000
    },
    {
        'id': 2,
        "name": "Test Account 2 (USD)",
        "currencyId": 1,
        "accountTypeId": 2,
        'initial_balance': 30_000,
        "balance": 30_000
    },
    {
        'id': 3,
        "name": "Test Account 1 (UAH)",
        "currencyId": 2,
        "accountTypeId": 2,
        'initial_balance': 1_000_000,
        "balance": 1_000_000
    },
    {
        'id': 4,
        "name": "Test Account 2 (UAH)",
        "currencyId": 2,
        "accountTypeId": 2,
        'initial_balance': 20_000,
        "balance": 20_000
    },
    {
        'id': 5,
        "name": "Test Account 1 (EUR)",
        "currencyId": 3,
        "accountTypeId": 2,
        'initial_balance': 250_000,
        "balance": 250_000
    },
    {
        'id': 6,
        "name": "Test Account 2 (EUR)",
        "currencyId": 3,
        "accountTypeId": 2,
        'initial_balance': 350_000,
        "balance": 350_000
    },
    {
        'id': 7,
        "name": "Test Account 1 (BGN)",
        "currencyId": 4,
        "accountTypeId": 1,
        'initial_balance': 0,
        "balance": 0
    },
    {
        'id': 8,
        "name": "Test Account 2 (BGN)",
        "currencyId": 4,
        "accountTypeId": 2,
        'initial_balance': 25_000,
        "balance": 25_000
    },
]
