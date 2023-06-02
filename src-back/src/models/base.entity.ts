import { Exclude } from 'class-transformer';
import { PrimaryGeneratedColumn, UpdateDateColumn, CreateDateColumn, BaseEntity, Column } from 'typeorm';

export class BaseModel extends BaseEntity {
    @PrimaryGeneratedColumn()
    id: number;

    @Column({ type: 'boolean', nullable: true, default: false })
    @Exclude()
    is_deleted: boolean;

    @Exclude()
    @CreateDateColumn({ type: 'timestamptz', default: () => 'CURRENT_TIMESTAMP' })
    created_at: Date;

    @Exclude()
    @UpdateDateColumn({ type: 'timestamptz', default: () => 'CURRENT_TIMESTAMP' })
    updated_at: Date;
}