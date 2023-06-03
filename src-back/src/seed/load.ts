import { loadDefaultCurrencies } from './currency-loader';
import {loadDefaultCategories} from './defaultcategory-loader'

async function seedData() {
  try {
    await loadDefaultCurrencies();
    await loadDefaultCategories();
    console.log('Initial data loading completed successfully.');
  } catch (error) {
    console.error('An error occurred during initial data loading:', error);
  }
}

seedData();
