import { Injectable } from '@nestjs/common';
import { DataSource } from 'typeorm';

import { UserCategory } from 'src/models/UserCategory.entity';

@Injectable()
export class CategoriesService {
  constructor(private dataSource: DataSource) { }

  async getUserCategories(request: Request): Promise<UserCategory[]> {
    const categories = await UserCategory.find({
      where: { user: { id: request['user'].id } },
      relations: ['parent'],
    });

    return categories;
  }
}
