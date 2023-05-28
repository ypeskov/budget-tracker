
import {
  BadRequestException,
  Body,
  Controller,
  Get,
  HttpCode,
  HttpStatus,
  Post,
  Request
} from '@nestjs/common';

import { AuthService } from './auth.service';
import { Public } from './public.decorator';
import { SignInDTO } from './signInDTO';
import { CreateUserDTO } from './createUser.DTO';
import { CommonResponse, ErrorResponse } from 'src/dto/common.response.dto';
import { plainToClass } from 'class-transformer';
import { User } from 'src/models/user.entity';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @HttpCode(HttpStatus.OK)
  @Public()
  @Post('login')
  signIn(@Body() signInDto: SignInDTO) {
    return this.authService.signIn(signInDto.email, signInDto.password);
  }

  @Get('profile')
  getProfile(@Request() req) {
    return req.user;
  }

  @Post('/user')
  @Public()
  async createUser(@Body() user: CreateUserDTO): Promise<CommonResponse> {
    console.log(user);
    try {
      const createdUser = await this.authService.createUser(user);
      const payload = plainToClass(User, createdUser);

      return new CommonResponse(true, payload);
    } catch(err: Error | any) {
      throw new BadRequestException(new CommonResponse(false, new ErrorResponse(
        err.code,
        err.message
      )));
    }
  }
}
