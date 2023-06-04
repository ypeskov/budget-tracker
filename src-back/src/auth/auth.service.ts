import { ConflictException, 
  Injectable, 
  UnauthorizedException } from '@nestjs/common';

import * as bcrypt from 'bcrypt'

import { UsersService } from '../modules/users/users.service';
import { JwtService } from '@nestjs/jwt';
import { User } from 'src/models/User.entity';
import { CreateUserDTO } from './createUser.DTO';
import { SignInDTO } from './signInDTO';
import { Currency } from 'src/models/Currency.entity';
import { DefaultCategory } from 'src/models/DefaultCategory.entity';
import { UserCategory } from 'src/models/UserCategory.entity';
import { MongoNetworkTimeoutError } from 'typeorm';


const saltRounds = 10;
const DEFAULT_CURRENCY_CODE = 'USD';

@Injectable()
export class AuthService {
  constructor(private usersService: UsersService,
              private jwtService: JwtService
    ) {}

  async createUser(user: CreateUserDTO): Promise<User> {
    try {
      const passwordHash = await bcrypt.hash(user.password, saltRounds);
      
      const newUser = new User();
      newUser.passwordHash = passwordHash;
      newUser.email = user.email;
      newUser.firstName = user.firstName;
      newUser.lastName = user.lastName;
      
      let currency: Currency = await Currency.findOneByOrFail({code: DEFAULT_CURRENCY_CODE});
  
      if (currency) {
        newUser.base_currency = currency;
      } else {
        console.log('Currency not found');
      }

      await newUser.save();
      this.copyAllCategories(newUser.id);
      
      return newUser;
    } catch (err) {
      if (err.code === '23505') {
        console.log(err);
        throw new ConflictException('User already exists');
      } else {
        console.log(err);
        throw err;
      }
    }
  }

  async signIn(userSignIn: SignInDTO): Promise<any> {
    const user = await this.usersService.findOneByEmail(userSignIn.email);

    if (! await bcrypt.compare(userSignIn.password, user.passwordHash)) {
      throw new UnauthorizedException();
    }
    const payload = {...user.toPlainObject()};
    
    return {
      access_token: await this.jwtService.signAsync(payload),
    };
  }

  async copyCategories(defaultCategory: DefaultCategory, 
                        userId: number, 
                        parentId?: number): Promise<void> {
    const newCategory = new UserCategory();
    newCategory.name = defaultCategory.name;
    newCategory.parent = {id: parentId} as UserCategory;
    newCategory.is_income = defaultCategory.is_income;
    newCategory.user = { id: userId } as User;
    await newCategory.save()

    if (defaultCategory.children) {
      for (const child of defaultCategory.children) {
        await this.copyCategories(child, userId, newCategory.id);
      }
    }
  }

  async copyAllCategories(userId: number): Promise<void> {
    const rootCategories = await DefaultCategory.find({
      where: { parent_id: null},
      relations: ['children']
    });
    for (const rootCategory of rootCategories) {
      await this.copyCategories(rootCategory, userId);
    }
  }
}
