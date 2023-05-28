import { Entity, Column } from "typeorm"
import { BaseModel } from "./base.entity"
import { Exclude } from "class-transformer";

@Entity({name: 'users'})
export class User extends BaseModel {
  
  @Exclude()
  private _email: string

  get email(): string {
    return this._email;
  }

  @Column({unique: true})
  set email(email: string) {
    if (!this.isValidEmail(email)) {
      throw new Error('Incorrect email');
    }
    this._email = email;
  }

  @Column({nullable: true})
  firstName: string | null

  @Column({nullable: true})
  lastName: string | null

  @Exclude()
  @Column({default: ''})
  passwordHash: string

  @Exclude()
  @Column({default: true})
  isActive: boolean = true

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}