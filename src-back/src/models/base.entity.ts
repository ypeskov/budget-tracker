import { Exclude } from 'class-transformer';
import { PrimaryGeneratedColumn, UpdateDateColumn, CreateDateColumn, BaseEntity } from 'typeorm';

export class BaseModel extends BaseEntity {
    @PrimaryGeneratedColumn()
    id: number;

    @Exclude()
    @CreateDateColumn({ type: 'timestamptz', default: () => 'CURRENT_TIMESTAMP' })
    created_at: Date;

    @Exclude()
    @UpdateDateColumn({ type: 'timestamptz', default: () => 'CURRENT_TIMESTAMP' })
    updated_at: Date;
}