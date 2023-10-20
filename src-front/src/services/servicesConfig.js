import { AccountService } from './accounts';
import { UserService } from './users';
import { CategoriesService } from './categories';
import { TransactionsService } from './transactions';
import { CurrenciesService } from './currencies';

import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';

const userStore = useUserStore();
const accountStore = useAccountStore();

const userService = new UserService(userStore);
const accountsService = new AccountService(accountStore, userService);
const categoriesService = new CategoriesService(userService);
const transactionsService = new TransactionsService(userService, accountsService);
const currenciesService = new CurrenciesService(userService);

userService.injectServices({
  accountsService,
  categoriesService,
  transactionsService,
  currenciesService,
});

export const Services = {
  userService,
  accountsService,
  categoriesService,
  transactionsService,
  currenciesService,
};

