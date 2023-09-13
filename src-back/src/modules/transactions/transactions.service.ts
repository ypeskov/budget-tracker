import { Injectable } from '@nestjs/common';

import { DataSource } from 'typeorm';
import { Transaction } from 'src/models/Transaction.entity';
import { Currency } from 'src/models/Currency.entity';
import { UserCategory } from 'src/models/UserCategory.entity';
import { User } from 'src/models/User.entity';
import { CreateTransactionDTO } from './DTO/CreateTransaction.dto';
import { Account } from 'src/models/Account.entity';

@Injectable()
export class TransactionsService {
  constructor(private dataSource: DataSource) {}

  async getTransactions(request: Request): Promise<Transaction[]> {
    const transactions = await Transaction.find({
      where: { user: { id: request['user'].id } },
    });

    return transactions;
  }

  async getTransactionDetails(id: string): Promise<Transaction | undefined> {
    const transaction = await Transaction.findOne({
      where: { id: parseInt(id) },
      relations: ['currency', 'category', 'account', 'target_account'],
    });

    return transaction;
  }

  async createTransaction(
    request: Request,
    newTransaction: CreateTransactionDTO,
  ) {
    const queryRunner = this.dataSource.createQueryRunner();

    let transaction = new Transaction();

    const currency: Currency = await Currency.findOneByOrFail({
      id: newTransaction.currency_id,
    });
    transaction.currency = currency;

    const category: UserCategory = await UserCategory.findOneByOrFail({
      id: newTransaction.category_id,
    });
    transaction.category = category;

    transaction.amount = newTransaction.amount;

    const account: Account = await Account.findOneByOrFail({
      id: newTransaction.account_id,
    });
    account.balance = Number(account.balance);
    transaction.account = account;
    transaction.account.balance += transaction.amount;

    const user: User = await User.findOneByOrFail({ id: request['user'].id });
    transaction.user = user;

    transaction.short_description = newTransaction.short_description;
    transaction.long_description = newTransaction.long_description;
    transaction.datetime = new Date();

    await queryRunner.connect();
    await queryRunner.startTransaction();

    try {
      await queryRunner.manager.save(transaction.account);
      await queryRunner.manager.save(transaction);
      await queryRunner.commitTransaction();
    } catch (err) {
      await queryRunner.rollbackTransaction();
      throw err;
    } finally {
      await queryRunner.release();
    }

    return transaction;
  }
}
