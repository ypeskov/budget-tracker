import { Injectable } from '@nestjs/common';
import { User } from 'src/models/user.entity';


@Injectable()
export class UsersService {
  async findOneByEmail(email: string): Promise<User | undefined> {
    return User.findOneByOrFail({ email: email });
  }
}
