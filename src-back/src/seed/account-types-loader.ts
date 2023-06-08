import dataSource from '../data-source';
import { AccountType } from '../models/AccountType.entity';

export async function loadDefaultAccountTypes() {
  try {
    await dataSource.initialize();

    const accTypeRepository = dataSource.getRepository(AccountType);

    const defaultValues = [
      { id: 1, name: 'Cash', is_credit: false },
      { id: 2, name: 'Savings Account', is_credit: false },
      { id: 3, name: 'Checking Account', is_credit: false },
      { id: 4, name: 'Credit Card', is_credit: true },
      { id: 5, name: 'Investment Account', is_credit: false },
      { id: 6, name: 'Loan Account', is_credit: true },
      { id: 7, name: 'Retirement Account', is_credit: false },
      { id: 8, name: 'Other', is_credit: false },
    ];

    const accTypes = defaultValues.map((value) => {
      let accType = new AccountType();
      // accType.id = value.id;
      // accType.name = value.name;
      // accType.is_credit = value.is_credit;
      Object.assign(accType, value);

      return accType;
    });

    await accTypeRepository.insert(accTypes);

    await dataSource.destroy();
    console.log('Default account types are loaded in DB');
  } catch (error) {
    console.error('Error while loading account types:', error);
  }
}


if (require.main === module) {
  loadDefaultAccountTypes();
}