import { request } from './requests';

export class TransactionsService {
  userService;
  accountService

  constructor(userService, accountService) {
    this.userService = userService;
    this.accountService = accountService;
  }

  async getUserTransactions(filters={}) {
    let transactionsUrl = '/transactions/?per_page=1000';

    if (filters.accountId) {
      transactionsUrl += `&accounts=${filters.accountId}`;
    }
    
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

  async updateTransaction(transactionDetails) {
    const transactionDetailsUrl = `/transactions/`;
    const updatedTransaction = await request(transactionDetailsUrl, {
                                        method: 'PUT',
                                        body: JSON.stringify(transactionDetails),
                                      }, 
                                      {userService: this.userService});
    this.accountService.setShouldUpdateAccountsList(true);
    return updatedTransaction;
  }
}
