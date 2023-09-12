import { request } from './requests';
import { HttpError } from '../errors/HttpError';

export class CategoriesService {
  userStore;

  constructor(userStore) {
    this.userStore = userStore;
  }

  async getUserCategories() {
    const categoriesUrl = '/categories';
    let response;
    try {
      response = await request(categoriesUrl);
    } catch (e) {
      throw new HttpError('Something went wrong');
    }

    if (response.status === 200) {
      try {
        const data = await response.json();
        return data.payload;
      } catch (e) {
        console.log(e);
      }
    } else if (response.status === 401) {
      this.userService.logOutUser();
      throw new HttpError('Unauthorized', 401);
    }
    return [];
  }
}
