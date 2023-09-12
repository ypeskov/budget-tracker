import {
  Entity,
  Column,
  Index,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Account } from './Account.entity';
import { UserCategory } from './UserCategory.entity';
import { Currency } from './Currency.entity';
import { BaseModel } from './base.entity';
import { User } from './User.entity';

const SHORT_DESCRIPTION_MAX_LENGTH: number = 50

@Entity({ name: 'transactions' })
export class Transaction extends BaseModel {
  @ManyToOne(() => Account)
  @JoinColumn({name: 'account_id'})
  account: Account;

  @ManyToOne(() => User)
  @JoinColumn({name: 'user_id'})
  user: User;

  @ManyToOne(() => UserCategory)
  @JoinColumn({name: 'category_id'})
  category: UserCategory;

  @ManyToOne(() => Currency)
  @JoinColumn({name: 'currency_id'})
  currency: Currency;

  @Column({ type: 'numeric', nullable: true })
  amount: number;

  @Column({ length: SHORT_DESCRIPTION_MAX_LENGTH })
  @Index()
  short_description: string;

  @Column({ nullable: true })
  long_description: string;

  @Column({ type: 'timestamp with time zone', nullable: true })
  @Index()
  datetime: Date;

  @Column({ type: 'numeric', nullable: true })
  exchange_rate: number;
}
