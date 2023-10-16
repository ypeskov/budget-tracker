import {DateTime} from 'luxon';

import { request } from './requests';
import { HttpError } from '../errors/HttpError';

export class AccountService {
  accountStore;
  userService;

  timeToCacheAccountsList = 600000; // miliseconds aka 10 minutes

  constructor(accountStore, userService) {
    this.accountStore = accountStore;
    this.userService = userService;
  }

  async getAllUserAccounts() {
    // need to make more clever logic of account list update from server
    const currentTime = DateTime.now();
    const deltaFromLastUpdate = currentTime - this.accountStore.lastUpdated;

    if (!this.accountStore.shouldUpdate 
      && (this.accountStore.accounts.length > 0 && deltaFromLastUpdate < this.timeToCacheAccountsList)) {
      return this.accountStore.accounts;
    }
    
    const accountsUrl = '/accounts/';
    const response = await request(accountsUrl);

    if (response.status === 200) {
      try {
        const accs = await response.json();
        this.accountStore.accounts.length = 0;
        this.accountStore.accounts.push(...accs);
        this.accountStore.lastUpdated = DateTime.now();
        this.setShouldUpdateAccountsList(false);
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

  setShouldUpdateAccountsList(shouldUpdate) {
    this.accountStore.shouldUpdate = shouldUpdate;
  }

  async createAccount(accountDetails) {
    const accountsUrl = '/accounts/';
    const response = await request(accountsUrl, {
      method: 'POST',
      body: JSON.stringify(accountDetails),
    });

    if (response.status === 200) {
      try {
        const createdAccount = response.json();
        this.setShouldUpdateAccountsList(true);
        return createdAccount;
      } catch (e) {
        console.log(e);
      }
    } else if (response.status === 401) {
      this.userService.logOutUser();
      throw new HttpError('Unauthorized', 401);
    } else {
      console.log(response);
    }
  }

  async getAccountTypes() {
    const accTypesUrl = '/accounts/types/';
    const response = await request(accTypesUrl);
    if (response.ok) {
      const types = await response.json();
      this.accountStore.accountTypes.length = 0;
      this.accountStore.accountTypes.push(...types);
      return this.accountStore.accountTypes;
    } else if (response.status === 401) {
      throw new HttpError('Unauthorized', 401);
    } else {
      console.log('Some error happened');
    }
    return [];
  }
}
