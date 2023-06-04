import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  Index,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  OneToMany,
  JoinColumn,
  PrimaryColumnCannotBeNullableError,
} from 'typeorm';

import { BaseModel } from "./base.entity"

@Entity({ name: 'default_categories' })
export class DefaultCategory extends BaseModel {
  @Column()
  @Index()
  name?: string;

  @ManyToOne(() => DefaultCategory, (category) => category.children)
  @JoinColumn({name: 'parent_id'})
  parent?: DefaultCategory = null;

  @OneToMany(() => DefaultCategory, (category) => category.parent)
  children: DefaultCategory[];

  @Column({ type: 'boolean', default: false, nullable: true })
  is_income: boolean = false;

}
