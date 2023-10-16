import { AccountService } from './accounts';
import { UserService } from './users';
import { CategoriesService } from './categories';
import { TransactionsService } from './transactions';
// import { CurrencyService } from './currencyService';

import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';

const userStore = useUserStore();
const accountStore = useAccountStore();

export const Services = {
  accountsService: new AccountService(accountStore),
  userService: new UserService(userStore),
  categoriesService: new CategoriesService(),
  transactionService: new TransactionsService(),
  // currencyService: new CurrencyService(),
};

