import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    Index,
    CreateDateColumn,
    UpdateDateColumn,
    ManyToOne,
    OneToMany,
  } from 'typeorm';
  import { User } from './User.entity';
  
@Entity({ name: 'user_categories' })
export class UserCategory {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  user_id: number;

  @ManyToOne(() => User, (user) => user.categories)
  user: User;

  @Column()
  name: string;

  @Column({ nullable: true })
  parent_id: number;

  @ManyToOne(() => UserCategory, (category) => category.subcategories)
  parent: UserCategory;

  @OneToMany(() => UserCategory, (category) => category.parent)
  subcategories: UserCategory[];

  @Column({ type: 'boolean', default: false })
  is_income: boolean;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
  