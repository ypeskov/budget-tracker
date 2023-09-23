import { UserService } from './users';
import { request } from './requests';
import { HttpError } from '../errors/HttpError';

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
    const accountsUrl = '/accounts/';
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
      throw new HttpError('Unauthorized', 401);
    }
    return [];
  }

  async getAccountDetails(accountId) {
    const accDetailsUrl = '/accounts/' + accountId;
    const response = await request(accDetailsUrl);
    if (response.ok) {
      const details = await response.json();
      return details;
    } else if (response.status === 401) {
      throw new HttpError('Unauthorized', 401);
    } else {
      console.log('Some error happened');
    }
    return [];
  }
}
