import { request } from './requests';
import { HttpError } from '../errors/HttpError';

export class CurrenciesService {
  _userService;

  constructor(userService) {
    this._userService = userService;
  }

  async getAllCurrencies() {
    const currenciesUrl = '/currencies/';
    let response;
    try {
      response = await request(currenciesUrl);
    } catch (e) {
      throw new HttpError('Something went wrong');
    }

    if (response.status === 200) {
      try {
        const data = await response.json();
        return data;
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
