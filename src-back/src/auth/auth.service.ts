import { Injectable, 
  InternalServerErrorException, 
  UnauthorizedException } from '@nestjs/common';

import * as bcrypt from 'bcrypt'

import { UsersService } from '../users/users.service';
import { JwtService } from '@nestjs/jwt';
import { User } from 'src/models/user.entity';
import { CreateUserDTO } from './createUser.DTO';


const saltRounds = 10;

@Injectable()
export class AuthService {
  constructor(private usersService: UsersService,
              private jwtService: JwtService
    ) {}

  async createUser(user: CreateUserDTO): Promise<any> {
    let passwordHash = '';

    try {
      passwordHash = await bcrypt.hash(user.password, saltRounds);
    } catch(err) {
      throw err;
    }

    let newUser = new User();
    newUser.passwordHash = passwordHash;
    newUser.email = user.email;
    newUser.firstName = user.firstName;
    newUser.lastName = user.lastName;

    try {
      await newUser.save();
    } catch(err) {
      if (err.code === '23505') {
        throw err;
      } else {
        throw new Error('Duplicate user');
      }
    }
    
    return newUser;
  }

  async signIn(username: string, pass: string): Promise<any> {
    const user = await this.usersService.findOne(username);
    if (user?.password !== pass) {
      throw new UnauthorizedException();
    }
    const payload = { sub: user.userId, username: user.username };
    
    return {
      access_token: await this.jwtService.signAsync(payload),
    };
  }
}
