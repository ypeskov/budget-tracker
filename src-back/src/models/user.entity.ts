import { Entity, Column } from "typeorm"
import { BaseModel } from "./base.entity"

@Entity({name: 'users'})
export class User extends BaseModel {
    private _email: string

    get email(): string {
      return this._email;
    }
    

    @Column()
    set email(email: string) {
      console.log('p1')
      console.log(email);
      if (!this.isValidEmail(email)) {
        throw new Error('Incorrect email');
      }
      this._email = email;
    }

    @Column({nullable: true})
    firstName: string | null

    @Column({nullable: true})
    lastName: string | null

    @Column({default: ''})
    passwordHash: string = ''

    @Column({default: true})
    isActive: boolean = true

    private isValidEmail(email: string): boolean {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      console.log(emailRegex.test(email));
      return emailRegex.test(email);
    }
}