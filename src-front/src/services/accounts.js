import {DateTime} from 'luxon';

import {request} from './requests';


export class AccountService {
  accountStore;
  userService;

  timeToCacheAccountsList = 600000; // miliseconds aka 10 minutes

  constructor(accountStore, userService) {
    this.accountStore = accountStore;
    this.userService = userService;
  }

  async getUserAccounts(includeHidden = false) {1
    // need to make more clever logic of account list update from server
    const currentTime = DateTime.now();
    const deltaFromLastUpdate = currentTime - this.accountStore.lastUpdated;

    if (!this.accountStore.shouldUpdate
      && (this.accountStore.accounts.length > 0 && deltaFromLastUpdate < this.timeToCacheAccountsList)) {
      return this.accountStore.accounts;
    }

    const accountsUrl = `/accounts/?includeHidden=${includeHidden ? 'true' : 'false'}`;

    const accounts = await request(accountsUrl, {}, { userService: this.userService });
    if (accounts) {
      this.accountStore.accounts.length = 0;
      this.accountStore.accounts.push(...accounts);
      this.accountStore.lastUpdated = DateTime.now();
      this.setShouldUpdateAccountsList(false);
      return this.accountStore.accounts;
    }
  }

  async getAccountDetails(accountId) {
    const accDetailsUrl = '/accounts/' + accountId;
    return await request(accDetailsUrl, {}, {userService: this.userService});
  }

  setShouldUpdateAccountsList(shouldUpdate) {
    this.accountStore.shouldUpdate = shouldUpdate;
  }

  async createAccount(accountDetails) {
    const accountsUrl = '/accounts/';
    const createdAccount = await request(accountsUrl, {
        method: 'POST',
        body: JSON.stringify(accountDetails),
      },
      {userService: this.userService});
    this.setShouldUpdateAccountsList(true);
    return createdAccount;
  }

  async getAccountTypes() {
    const accTypesUrl = '/accounts/types/';
    const types = await request(accTypesUrl, {}, {userService: this.userService});
    this.accountStore.accountTypes.length = 0;
    this.accountStore.accountTypes.push(...types);
    return this.accountStore.accountTypes;
  }

  async deleteAccount(accountId) {
    const accUrl = '/accounts/' + accountId;
    await request(accUrl, {
      method: 'DELETE',
    }, {userService: this.userService});
    this.setShouldUpdateAccountsList(true);
  }

  async updateAccount(accountDetails) {
    const accUrl = '/accounts/' + accountDetails.id;
    await request(accUrl, {
      method: 'PUT',
      body: JSON.stringify(accountDetails),
    }, {userService: this.userService});
    this.setShouldUpdateAccountsList(true);
  }

  clearAccounts() {
    this.accountStore.accounts.length = 0;
    this.accountStore.lastUpdated = null;
    this.accountStore.shouldUpdate = true;
  }
}
