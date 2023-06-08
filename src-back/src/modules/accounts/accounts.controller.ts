import { Controller, Post, Request, Body } from '@nestjs/common';
import { AccountsService } from './accounts.service';
import { CreateAccountDTO } from './DTO/CreateAccount.dto';

@Controller('accounts')
export class AccountsController {
  constructor(private accService: AccountsService) {}

  @Post('/')
  async addAccount(@Request() request, @Body() newAccount: CreateAccountDTO): Promise<any> {
    const account = await this.accService.createAccount(newAccount, request['user']);

    return account.toPlainObject();
  }
}
