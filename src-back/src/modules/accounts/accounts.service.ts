import { Injectable } from '@nestjs/common';
import { CreateAccountDTO } from './DTO/CreateAccount.dto';
import { Account } from '../../models/Account.entity';
import { Currency } from 'src/models/Currency.entity';
import { User } from 'src/models/User.entity';
import { AccountType } from 'src/models/AccountType.entity';

@Injectable()
export class AccountsService {
  async createAccount(newAcc: CreateAccountDTO, user: User): Promise<Account> {
    const account = new Account();

    account.name = newAcc.name;
    account.currency = await Currency.findOneByOrFail({id: newAcc.currencyId});
    account.user = await User.findOneByOrFail({id: user.id});
    account.account_type = await AccountType.findOneByOrFail({id: newAcc.accountTypeId});
    account.initial_balance = newAcc.initialBalance ?? 0;
    account.balance = account.initial_balance;
    account.opening_date = newAcc.openingDate ? new Date(newAcc.openingDate) : (new Date());
    account.comment = newAcc.comment ?? '';
    account.opening_exchange_rate = newAcc.opening_exchane_rate ?? 0;

    await account.save();

    return account;
  }
 
  async getAccounts(user: User) {
    const accounts = await Account.find({where: {user: {id: user.id }}});

    return accounts;
  }

  async getAccountDetails(accountId: string): Promise<Account> {
    const account = await Account.findOneByOrFail({id: parseInt(accountId)});
    return account;
  }
}
