
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
import { CommonResponse } from 'src/dto/common.response.dto';


@Controller('auth') 
export class AuthController {
  constructor(private authService: AuthService) {}

  @HttpCode(HttpStatus.OK)
  @Public()
  @Post('login')
  signIn(@Body() userSignIn: SignInDTO) {
    return this.authService.signIn(userSignIn);
  }

  @Get('profile')
  getProfile(@Request() req) {
    return req.user;
  }

  @Post('/user')
  @Public()
  async createUser(@Body() user: CreateUserDTO): Promise<CommonResponse> {
    const createdUser = await this.authService.createUser(user);
    const payload = createdUser.toPlain();

    return new CommonResponse(true, payload);
  }
}
