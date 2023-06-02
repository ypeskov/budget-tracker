import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    Index,
    CreateDateColumn,
    UpdateDateColumn,
  } from 'typeorm';
  
@Entity({ name: 'currencies' })
export class Currency {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  @Index()
  code: string;

  @Column()
  @Index()
  name: string;

  @Column({ type: 'boolean', nullable: true, default: false })
  is_deleted: boolean;

  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;
}
