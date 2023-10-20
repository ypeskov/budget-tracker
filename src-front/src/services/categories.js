import { request } from './requests';

export class CategoriesService {
  userService;

  constructor(userService) {
    this.userService = userService;
  }

  async getUserCategories() {
    const categoriesUrl = '/categories/';
    return await request(categoriesUrl, {}, {userService: this.userService});
  }
}
