import {
    Entity,
    Column,
    Index,
    ManyToOne,
    JoinColumn,
  } from 'typeorm';

import { BaseModel } from './base.entity';
  
const ACCOUNT_TYPE_NAME_MAX_LENGTH: number = 100

@Entity({ name: 'account_types' })
export class AccountType extends BaseModel {
  @Column({ length: ACCOUNT_TYPE_NAME_MAX_LENGTH })
  @Index()
  name: string;

  @Column({ type: 'boolean', nullable: false, default: false })
  is_credit: boolean;
}
