import { createConnection } from 'typeorm';
import { Currency } from '../models/Currency.entity';
import { dataSourceOptions } from '../data-source';

export async function loadDefaultCurrencies() {
  try {
    const connectionOptions = dataSourceOptions;

    const connection = await createConnection(connectionOptions);
    const currencyRepository = connection.getRepository(Currency);

    const defaultValues = [
      { id: 1, code: 'USD', name: 'United States Dollar' },
      { id: 2, code: 'UAH', name: 'Ukrainian Hryvna' },
      { id: 3, code: 'EUR', name: 'Euro' },
      { id: 4, code: 'BGN', name: 'Bulgarian Lev' },
    ];

    const currencies = defaultValues.map((value) => {
      const currency = new Currency();
      currency.id = value.id;
      currency.code = value.code;
      currency.name = value.name;
      return currency;
    });

    await currencyRepository.save(currencies);

    await connection.destroy();
    console.log('Default currencies are loaded in DB');
  } catch (error) {
    console.error('Error while loading currencies:', error);
  }
}

loadDefaultCurrencies();
