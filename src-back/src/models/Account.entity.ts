import {
    Entity,
    Column,
    Index,
    ManyToOne,
    JoinColumn,
  } from 'typeorm';
import { Exclude, instanceToPlain } from "class-transformer";
import { AccountType } from './AccountType.entity';
import { Currency } from './Currency.entity';
import { User } from './User.entity';
import { BaseModel } from './base.entity';
  
const ACCOUNT_NAME_MAX_LENGTH: number = 100;

@Entity({ name: 'accounts' })
export class Account extends BaseModel {
  @ManyToOne(() => User, (user) => user.accounts)
  @JoinColumn({name: 'user_id'})
  user: User;

  @ManyToOne(() => AccountType)
  @JoinColumn({name: 'account_type_id'})
  account_type: AccountType;

  @ManyToOne(() => Currency)
  @JoinColumn({name: 'currency_id'})
  currency: Currency;

  @Column({ type: 'numeric', nullable: true })
  balance: number;

  @Column({ length: ACCOUNT_NAME_MAX_LENGTH })
  @Index()
  name: string;

  @Column({ type: 'timestamp', nullable: true })
  opening_date: Date;

  @Column({ type: 'numeric', nullable: true })
  initial_balance: number;

  @Column({ type: 'numeric', nullable: true })
  opening_exchange_rate: number;

  @Column({ nullable: true })
  comment: string;

  toPlainObject() {
    const plainUser = instanceToPlain(this);
    plainUser.user.email = this.user.email;

    return plainUser;
  }

  async updateBalance(amount: number) {
    this.balance = this.balance + amount;
    this.save();
  }
}
