import { createConnection } from 'typeorm';
import { dataSourceOptions } from '../data-source';
import { loadDefaultCurrencies } from './currency-loader';

async function seedData() {
  try {
    const connection = await createConnection(dataSourceOptions);

    // Запускаем каждый лоадер
    await loadDefaultCurrencies();
    // Вызывайте другие функции лоадеров по мере необходимости

    await connection.close();
    console.log('Initial data loading completed successfully.');
  } catch (error) {
    console.error('An error occurred during initial data loading:', error);
  }
}

seedData();
