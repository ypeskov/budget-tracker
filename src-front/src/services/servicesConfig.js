import { AccountService } from './accounts';
import { UserService } from './users';
import { CategoriesService } from './categories';
import { TransactionsService } from './transactions';

import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';

const userStore = useUserStore();
const accountStore = useAccountStore();

const userService = new UserService(userStore);
const accountService = new AccountService(accountStore, userService);
const categoriesService = new CategoriesService(userStore);
const transactionsService = new TransactionsService(userService, accountService);

export const Services = {
  userService: userService,
  accountsService: accountService,
  categoriesService: categoriesService,
  transactionService: transactionsService,
};

