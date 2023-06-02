import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  Index,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
} from 'typeorm';
import { Currency } from './Currency.entity';

@Entity({ name: 'exchange_rates' })
export class ExchangeRateHistory {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  from_currency_id: number;

  @ManyToOne(() => Currency, { eager: true })
  from_currency: Currency;

  @Column()
  to_currency_id: number;

  @ManyToOne(() => Currency, { eager: true })
  to_currency: Currency;

  @Column({ type: 'numeric', nullable: true })
  rate: number;

  @Column({ type: 'timestamp with time zone', nullable: false })
  @Index()
  datetime: Date;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
