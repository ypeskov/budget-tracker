
import {
  Body,
  Controller,
  Get,
  HttpCode,
  HttpStatus,
  Post,
  Request
} from '@nestjs/common';

// import { AuthGuard } from './auth.guard';
import { AuthService } from './auth.service';
import { Public } from './public.decorator';
import { SignInDTO } from './signInDTO';
import { CreateUserDTO } from './createUser.DTO';

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
  async createUser(@Body() user: CreateUserDTO) {
    try {
      return await this.authService.createUser(user);
    } catch(err: any) {
      console.log(err.message);
      return err.message;
    }
    
  }
}
