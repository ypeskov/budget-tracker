import { ConflictException, 
  Injectable, 
  UnauthorizedException } from '@nestjs/common';

import * as bcrypt from 'bcrypt'

import { UsersService } from '../users/users.service';
import { JwtService } from '@nestjs/jwt';
import { User } from 'src/models/user.entity';
import { CreateUserDTO } from './createUser.DTO';
import { SignInDTO } from './signInDTO';


const saltRounds = 10;

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

      await newUser.save();

      return newUser;
    } catch (err) {
      if (err.code === '23505') {
        throw new ConflictException('User already exists');
      } else {
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
}
