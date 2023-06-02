import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
} from 'typeorm';
import { Account } from './Account.entity';

@Entity({ name: 'credit_account_details' })
export class CreditAccountDetails {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  account_id: number;

  @ManyToOne(() => Account)
  account: Account;

  @Column({ type: 'numeric', nullable: true })
  own_balance: number;

  @Column({ type: 'numeric', nullable: true })
  credit_balance: number;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
