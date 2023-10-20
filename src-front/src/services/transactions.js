import { request } from './requests';

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
                                      }, 
                                      {userService: this.userService});
    this.accountService.setShouldUpdateAccountsList(true);
    return createdTransaction;
  }
}
