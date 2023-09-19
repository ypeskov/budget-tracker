import { UserService } from './users';
import { request } from './requests';
import { HttpError } from '../errors/HttpError';

export class TransactionsService {
  userService;

  constructor(userService) {
    this.userService = userService;
  }

  async getUserTransactions() {
    const transactionsUrl = '/transactions';
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
    }
    return [];
  }

  async addTransaction(transactionDetails) {
    const transactionDetailsUrl = `/transactions`;

    try {
      const response = await request(transactionDetailsUrl, {
        method: 'POST',
        body: JSON.stringify(transactionDetails)
      });

      if (response.status === 200) {
        try {
          const createdTransaction = response.json();
          console.log(createdTransaction);
        } catch(e) {
          console.log(e);
        }
      }
    } catch(e) {
      console.log(e);
    }
    

    
  }
}
