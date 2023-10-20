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
    return await request(transactionsUrl, {}, {userService: this.userService});
  }

  async getTransactionDetails(id) {
    const transactionDetailsUrl = '/transactions/' + id;
    return await request(transactionDetailsUrl, {}, {userService: this.userService});
  }

  async addTransaction(transactionDetails) {
    const transactionDetailsUrl = `/transactions`;
    const createdTransaction = await request(transactionDetailsUrl, {
      method: 'POST',
      body: JSON.stringify(transactionDetails),
    });
    this.accountService.setShouldUpdateAccountsList(true);
    return createdTransaction;

  //   try {
      

  //     if (response.status === 200) {
  //       try {
  //         const createdTransaction = response.json();
  //         this.accountService.setShouldUpdateAccountsList(true);
  //         return createdTransaction;
  //       } catch (e) {
  //         console.log(e);
  //       }
  //     } else if (response.status === 401) {
  //       this.userService.logOutUser();
  //       throw new HttpError('Unauthorized', 401);
  //     } else {
  //       console.log(response);
  //     }
  //     return null;
  //   } catch (e) {
  //     console.log(e);
  //   }
  }
}
