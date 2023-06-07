import { Injectable,
  Request } from '@nestjs/common';

import { Transaction } from 'src/models/Transaction.entity';
import { Currency } from 'src/models/Currency.entity';
import { UserCategory } from 'src/models/UserCategory.entity';
import { User } from 'src/models/User.entity';

@Injectable()
export class TransactionsService {
  async createTransaction(request: Request) {
    let transaction = new Transaction();

    const currency: Currency = await Currency.findOneByOrFail({code: 'USD'});
    transaction.currency = currency;

    const category: UserCategory = await UserCategory.findOneByOrFail({id: 1});
    transaction.category = category;

    const user: User = await User.findOneByOrFail({id: request['user'].id})
    transaction.user = user;

    transaction.amount_in_currency = 100;

    transaction.short_description = 'ololoo';
    transaction.long_description = 'FUFUFUF';
    transaction.datetime = new Date();

    transaction.save();

    return transaction;
  }
}
