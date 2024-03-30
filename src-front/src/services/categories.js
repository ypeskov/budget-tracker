import { request } from './requests';

const categoriesUrlPrefix = '/categories';

export class CategoriesService {
  userService;

  constructor(userService) {
    this.userService = userService;
  }

  async getUserCategories() {
    const categoriesUrl = `${categoriesUrlPrefix}/`;
    return await request(categoriesUrl, {}, {userService: this.userService});
  }

  async getGroupedCategories() {
    const categoriesUrl = `${categoriesUrlPrefix}/grouped/`;
    return await request(categoriesUrl, {}, {userService: this.userService});
  }
}
