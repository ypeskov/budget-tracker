import { Controller, 
  Post, 
  Request } from '@nestjs/common';
import { TransactionsService } from './transactions.service';
import { CommonResponse } from 'src/dto/common.response.dto';

@Controller('transactions')
export class TransactionsController {
  constructor(private transactionsService: TransactionsService) {}

  @Post('/')
  async addTransaction(@Request() request): Promise<CommonResponse> {
    const transaction = await this.transactionsService.createTransaction(request);

    return new CommonResponse(true, transaction);
  }
}
