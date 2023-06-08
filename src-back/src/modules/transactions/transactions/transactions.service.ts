import { Injectable,
  Request } from '@nestjs/common';

import { Transaction } from 'src/models/Transaction.entity';
import { Currency } from 'src/models/Currency.entity';
import { UserCategory } from 'src/models/UserCategory.entity';
import { User } from 'src/models/User.entity';
import { CreateTransactionDTO } from '../DTO/CreateTransaction.dto';

@Injectable()
export class TransactionsService {
  async createTransaction(request: Request, newTransaction: CreateTransactionDTO) {
    let transaction = new Transaction();

    const currency: Currency = await Currency.findOneByOrFail({id: newTransaction.currency_id});
    transaction.currency = currency;

    const category: UserCategory = await UserCategory.findOneByOrFail({id: newTransaction.category_id});
    transaction.category = category;

    const user: User = await User.findOneByOrFail({id: request['user'].id})
    transaction.user = user;

    transaction.amount = 100;

    transaction.short_description = newTransaction.short_description;
    transaction.long_description = newTransaction.long_description;
    transaction.datetime = new Date();

    transaction.save();

    return transaction;
  }
}
