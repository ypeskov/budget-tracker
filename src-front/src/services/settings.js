import { toRaw } from 'vue';
import { request } from './requests';

const settingsPrefixUrl = '/settings';

export class SettingsService {
  userService;

  constructor(userService) {
    this.userService = userService;
  }

  async getLanguages() {
    const languagesUrl = `${settingsPrefixUrl}/languages/`;
    return await request(languagesUrl, {}, { userService: this.userService });
  }

  async saveUserSettings(settings = null) {
    const saveUserSettingsUrl = `${settingsPrefixUrl}/`;
    if (settings === null) {
      settings = toRaw(this.userService.userStore.settings);
    }

    this.updateSettingsInStorage(settings);

    return await request(saveUserSettingsUrl,
      {
        method: 'POST',
        body: JSON.stringify({
          settings: settings,
        }),
      },
      { userService: this.userService });
  }

  updateSettingsInStorage(settings) {
    const user = JSON.parse(localStorage.getItem('user'));
    user.settings = settings;
    localStorage.setItem('user', JSON.stringify(user));

    return user;
  }
}
