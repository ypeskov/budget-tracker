import { request } from './requests';

const categoriesUrlPrefix = '/categories';

export class CategoriesService {
  userService;

  constructor(userService) {
    this.userService = userService;
  }

  async getUserCategories() {
    const categoriesUrl = `${categoriesUrlPrefix}/`;
    return await request(categoriesUrl, {}, { userService: this.userService });
  }

  async getGroupedCategories() {
    const categoriesUrl = `${categoriesUrlPrefix}/grouped/`;
    return await request(categoriesUrl, {}, { userService: this.userService });
  }

  async updateCategory(category) {
    const categoriesUrl = `${categoriesUrlPrefix}/${category.id}/`;
    return await request(categoriesUrl, {
      method: 'PUT',
      body: JSON.stringify(category),
    }, { userService: this.userService });
  }

  async createCategory(category) {
    const categoriesUrl = `${categoriesUrlPrefix}/`;
    return await request(categoriesUrl, {
      method: 'POST',
      body: JSON.stringify(category),
    }, { userService: this.userService });
  }

  async deleteCategory(categoryId) {
    const categoriesUrl = `${categoriesUrlPrefix}/${categoryId}/`;
    return await request(categoriesUrl, {
      method: 'DELETE',
    }, { userService: this.userService });
  }
}
