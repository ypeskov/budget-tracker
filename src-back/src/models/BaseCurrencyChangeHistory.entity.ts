import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    Index,
    CreateDateColumn,
    UpdateDateColumn,
    ManyToOne,
  } from 'typeorm';
  import { User } from './User.entity';
  import { Currency } from './Currency.entity';
  
@Entity({ name: 'base_currency_change_history' })
export class BaseCurrencyChangeHistory {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  user_id: number;

  @ManyToOne(() => User)
  user: User;

  @Column()
  base_currency_id: number;

  @ManyToOne(() => Currency)
  base_currency: Currency;

  @Column({ type: 'timestamp with time zone', nullable: false })
  @Index()
  change_date_time: Date;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
  