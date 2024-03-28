import { request } from './requests';

const settingsPrefixUrl = '/settings';

export class SettingsService {
  userService;

  constructor(userService) {
    this.userService = userService;
  }

  async getLanguages() {
    const languagesUrl = `${settingsPrefixUrl}/languages/`;
    return await request(languagesUrl, {}, {userService: this.userService});
  }
}