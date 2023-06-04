import {
    Entity,
    ManyToOne,
    Column,
    Index,
    JoinColumn
  } from 'typeorm';

import { BaseModel } from "./base.entity";
import {User} from './User.entity';
  
@Entity({ name: 'currencies' })
export class Currency extends BaseModel {
  @Column()
  @Index()
  code: string;

  @Column()
  @Index()
  name: string;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;
}
