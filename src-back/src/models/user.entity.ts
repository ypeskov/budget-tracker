import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  Index,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
  ManyToOne,
} from 'typeorm';
import { Exclude, instanceToPlain } from "class-transformer";

import { BaseModel } from "./base.entity"
import { Account } from './Account.entity';
import { Currency } from './Currency.entity';
import { UserCategory } from './UserCategory.entity';
import { ErrorResponse } from "../dto/common.response.dto";

@Entity({ name: 'users' })
export class User extends BaseModel {
  @PrimaryGeneratedColumn()
  id: number;

  @Exclude()
  _email: string

  get email(): string {
    return this._email;
  }

  @Column({unique: true})
  @Index()
  set email(email: string) {
    if (!this.isValidEmail(email)) {
      throw new ErrorResponse(400, 'Incorrect Email');
    }
    this._email = email;
  }

  @Column()
  @Index()
  firstName: string;

  @Column()
  @Index()
  lastName: string;

  @Column()
  @Exclude()
  passwordHash: string;

  @Column({ type: 'boolean', default: true })
  @Exclude()
  is_active: boolean;

  @ManyToOne(() => Currency)
  @Exclude()
  base_currency: Currency;

  @OneToMany(() => Account, (account) => account.user)
  accounts: Account[];

  @OneToMany(() => UserCategory, (category) => category.user)
  categories: UserCategory[];



  @CreateDateColumn({ type: 'timestamp with time zone', nullable: false })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone', nullable: false })
  updated_at: Date;

  toPlainObject() {
    const plainUser = instanceToPlain(this);
    return { ...plainUser, email: this.email };
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}
