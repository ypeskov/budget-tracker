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

@Entity({ name: 'default_categories' })
export class DefaultCategory {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  @Index()
  name: string;

  @Column({ nullable: true })
  parent_id: number;

  @ManyToOne(() => DefaultCategory, (category) => category.children)
  parent: DefaultCategory;

  @OneToMany(() => DefaultCategory, (category) => category.parent)
  children: DefaultCategory[];

  @Column({ type: 'boolean', default: false })
  is_income: boolean;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
