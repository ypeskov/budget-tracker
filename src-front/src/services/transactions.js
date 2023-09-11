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
        // console.log(transactions.payload);
        return transactions.payload;
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
        return transactionDetails.payload;
      } catch (e) {
        console.log(e);
      }
    } else if (response.status === 401) {
      this.userService.logOutUser();
      throw new HttpError('Unauthorized', 401);
    }
    return [];
  }
}
