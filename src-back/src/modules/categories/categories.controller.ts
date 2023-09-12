import { Controller, Get, Request } from '@nestjs/common';

import { CategoriesService } from './categories.service';
import { CommonResponse } from 'src/dto/common.response.dto';


@Controller('categories')
export class CategoriesController {
  constructor(private categoriesService: CategoriesService) { }

  @Get('/')
  async getTransactionsByUserId(@Request() request): Promise<CommonResponse> {
    const transations = await this.categoriesService.getUserCategories(request);
    return new CommonResponse(true, transations);
  }
}
