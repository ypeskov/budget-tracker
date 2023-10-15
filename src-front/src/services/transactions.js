import { request } from './requests';
import { HttpError } from '../errors/HttpError';

export class TransactionsService {
  userService;
  accountService

  constructor(userService, accountService) {
    this.userService = userService;
    this.accountService = accountService;
  }

  async getUserTransactions() {
    const transactionsUrl = '/transactions/?per_page=1000';
    const response = await request(transactionsUrl);

    if (response.status === 200) {
      try {
        const transactions = await response.json();
        return transactions;
      } catch (e) {
        console.log(e);
      }
    } else if (response.status === 401) {
      this.userService.logOutUser();
      throw new HttpError('Unauthorized', 401);
    } else {
      console.log(response);
    }
    return [];
  }

  async getTransactionDetails(id) {
    const transactionDetailsUrl = '/transactions/' + id;
    const response = await request(transactionDetailsUrl);

    if (response.status === 200) {
      try {
        const transactionDetails = await response.json();
        return transactionDetails;
      } catch (e) {
        console.log(e);
      }
    } else if (response.status === 401) {
      this.userService.logOutUser();
      throw new HttpError('Unauthorized', 401);
    } else {
      console.log(response);
    }
    return [];
  }

  async addTransaction(transactionDetails) {
    const transactionDetailsUrl = `/transactions`;

    try {
      const response = await request(transactionDetailsUrl, {
        method: 'POST',
        body: JSON.stringify(transactionDetails),
      });

      if (response.status === 200) {
        try {
          const createdTransaction = response.json();
          this.accountService.setShouldUpdateAccountsList(true);
          return createdTransaction;
        } catch (e) {
          console.log(e);
        }
      } else if (response.status === 401) {
        this.userService.logOutUser();
        throw new HttpError('Unauthorized', 401);
      } else {
        console.log(response);
      }
      return null;
    } catch (e) {
      console.log(e);
    }
  }
}
