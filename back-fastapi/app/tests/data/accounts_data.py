test_account_types = [
    {'id': 1, 'name': 'cash', 'is_credit': False},
    {'id': 2, 'name': 'regular_bank', 'is_credit': False},
    {'id': 3, 'name': 'debit_card', 'is_credit': False},
    {'id': 4, 'name': 'credit_card', 'is_credit': True},
    {'id': 5, 'name': 'loan', 'is_credit': True},
]

test_accounts_data = [
    {
        'id': 3,
        "name": "Test Account 1 (UAH)",
        "currencyId": 2,
        "accountTypeId": 2,
        'initial_balance': 1_000_000,
        "balance": 1_000_000,
    },
    {
        'id': 1,
        "name": "Test Account 1 (USD)",
        "currencyId": 1,
        "accountTypeId": 2,
        'initial_balance': 500_000,
        "balance": 500_000,
    },
    {
        'id': 2,
        "name": "Test Account 2 (USD)",
        "currencyId": 1,
        "accountTypeId": 2,
        'initial_balance': 30_000,
        "balance": 30_000,
    },
]
