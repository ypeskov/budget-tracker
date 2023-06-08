import { Controller, 
  Post, 
  Body,
  Request } from '@nestjs/common';
import { TransactionsService } from './transactions.service';
import { CommonResponse } from 'src/dto/common.response.dto';
import { CreateTransactionDTO } from '../DTO/CreateTransaction.dto';

@Controller('transactions')
export class TransactionsController {
  constructor(private transactionsService: TransactionsService) {}

  @Post('/')
  async addTransaction(@Request() request, 
              @Body() newTransaction: CreateTransactionDTO): Promise<CommonResponse> {
    const transaction = await this.transactionsService.createTransaction(request, newTransaction);

    return new CommonResponse(true, transaction);
  }
}
