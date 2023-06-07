import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  Index,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
} from 'typeorm';
import { Account } from './Account.entity';
import { UserCategory } from './UserCategory.entity';
import { Currency } from './Currency.entity';
import { BaseModel } from './base.entity';

const SHORT_DESCRIPTION_MAX_LENGTH: number = 50

@Entity({ name: 'transactions' })
export class Transaction extends BaseModel {
  @ManyToOne(() => Account)
  account: Account;

  @ManyToOne(() => UserCategory)
  category: UserCategory;

  @ManyToOne(() => Currency)
  currency: Currency;

  @Column({ type: 'numeric', nullable: true })
  amount_in_currency: number;

  @Column({ length: SHORT_DESCRIPTION_MAX_LENGTH })
  @Index()
  short_description: string;

  @Column({ nullable: true })
  long_description: string;

  @Column({ type: 'timestamp with time zone', nullable: false })
  @Index()
  datetime: Date;

  @Column({ type: 'numeric', nullable: true })
  exchange_rate: number;
}
