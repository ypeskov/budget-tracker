import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    ManyToOne,
    OneToMany,
    JoinColumn,
  } from 'typeorm';
import { User } from './User.entity';
import { BaseModel } from "./base.entity"
  
@Entity({ name: 'user_categories' })
export class UserCategory extends BaseModel{
  @ManyToOne(() => User, (user) => user.categories)
  @JoinColumn({name: 'user_id'})
  user: User;

  @Column()
  name: string;

  @ManyToOne(() => UserCategory, (category) => category.subcategories)
  @JoinColumn({name: 'parent_id'})
  parent: UserCategory;

  @OneToMany(() => UserCategory, (category) => category.parent)
  subcategories: UserCategory[];

  @Column({ type: 'boolean', default: false })
  is_income: boolean;  
}
  