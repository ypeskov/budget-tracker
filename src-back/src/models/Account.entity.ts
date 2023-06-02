import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    Index,
    CreateDateColumn,
    UpdateDateColumn,
    ManyToOne,
    RelationId,
  } from 'typeorm';
  import { AccountType } from './AccountType.entity';
  import { Currency } from './Currency.entity';
  import { User } from './User.entity';
  
const ACCOUNT_NAME_MAX_LENGTH: number = 100;

@Entity({ name: 'accounts' })
export class Account {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  user_id: number;

  @ManyToOne(() => User, (user) => user.accounts)
  user: User;

  @Column()
  account_type_id: number;

  @ManyToOne(() => AccountType)
  account_type: AccountType;

  @Column()
  currency_id: number;

  @ManyToOne(() => Currency)
  currency: Currency;

  @Column({ type: 'numeric', nullable: true })
  balance: number;

  @Column({ length: ACCOUNT_NAME_MAX_LENGTH })
  @Index()
  name: string;

  @Column({ type: 'date', nullable: true })
  opening_date: Date;

  @Column({ type: 'numeric', nullable: true })
  initial_balance_in_currency: number;

  @Column({ type: 'numeric', nullable: true })
  opening_exchange_rate: number;

  @Column({ nullable: true })
  comment: string;

  @Column({ type: 'boolean', default: true })
  show_in_transactions: boolean;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
