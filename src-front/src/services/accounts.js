import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';
import { UserService } from './users';
import { request } from './requests';

export class AccountService {
  userStore;
  accountStore;

  userService;

  constructor(userStore, accountStore) {
    this.userStore = userStore;
    this.accountStore = accountStore;
    this.userService = new UserService(userStore);
  }

  async getAllUserAccounts() {
    const accountsUrl = 'http://localhost:9000/accounts';
    const response = await request(accountsUrl);

    if (response.status === 200) {
      try {
        const accs = await response.json();
        this.accountStore.accounts.length = 0;
        this.accountStore.accounts.push(...accs);
        return this.accountStore.accounts;
      } catch (e) {
        console.log(e);
      }
    } else if (response.status === 401) {
      this.userService.logOutUser();
      throw new Error('Unauthorized');
    }
    return [];
  }
}
