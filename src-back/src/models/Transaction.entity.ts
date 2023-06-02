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

const SHORT_DESCRIPTION_MAX_LENGTH: number = 50

@Entity({ name: 'transactions' })
export class Transaction {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  account_id: number;

  @ManyToOne(() => Account)
  account: Account;

  @Column()
  category_id: number;

  @ManyToOne(() => UserCategory)
  category: UserCategory;

  @Column()
  currency_id: number;

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

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
