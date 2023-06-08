import { loadDefaultCurrencies } from './currency-loader';
import {loadDefaultCategories} from './defaultcategory-loader';
import { loadDefaultAccountTypes } from './account-types-loader';

async function seedData() {
  try {
    await loadDefaultCurrencies();
    await loadDefaultCategories();
    await loadDefaultAccountTypes();
    
    console.log('Initial data loading completed successfully.');
  } catch (error) {
    console.error('An error occurred during initial data loading:', error);
  }
}

seedData();
