import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    Index,
    CreateDateColumn,
    UpdateDateColumn,
  } from 'typeorm';
  
const ACCOUNT_TYPE_NAME_MAX_LENGTH: number = 100

@Entity({ name: 'account_types' })
export class AccountType {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: ACCOUNT_TYPE_NAME_MAX_LENGTH })
  @Index()
  type_name: string;

  @Column({ type: 'boolean', nullable: false, default: false })
  is_credit: boolean;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
