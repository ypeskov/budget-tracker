import { request } from './requests';

export class UserService {
  userStore;

  accountsService;
  transactionsService;
  categoriesService;
  currenciesService;

  constructor(userStore) {
    this.userStore = userStore;
  }

  injectServices(services={}) {
    for (const [serviceName, service] of Object.entries(services)) {
      this[serviceName] = service;
    }
  }

  async loginUser(loginEmail, password) {
    const loginPath = '/auth/login/';
    const requestBody = {
      email: loginEmail,
      password,
    };
    try {
      const response = await request(loginPath, {
        method: 'POST',
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      if (data.access_token) {
        this.userStore.accessToken = data.access_token;
        this.getUserProfile(this.userStore.accessToken);
        this.accountsService.getAllUserAccounts();
      } else {
        alert('Something went wrong!');
      }
    } catch (e) {
      console.log(e);
    }
  }

  async getUserProfile(accessToken) {
    try {
      const profileEndpoint = '/auth/profile/';
      const response = await request(profileEndpoint);
      const userProfile = await response.json();
      this.setUser(userProfile, true, accessToken);
    } catch (e) {
      console.log(e);
    }
  }

  setUser(userProfile, isLoggedIn = false, accessToken = '') {
    // need to make deep copying to avoid cycling errors
    const clonedUserProfile = JSON.parse(JSON.stringify(userProfile));
    this.userStore.user = Object.assign(this.userStore.user, clonedUserProfile);

    this.userStore.isLoggedIn = isLoggedIn;
    this.userStore.accessToken = accessToken;

    localStorage.setItem('user', JSON.stringify(this.userStore.user));
    localStorage.setItem('isLoggedIn', this.userStore.isLoggedIn);
    localStorage.setItem('accessToken', this.userStore.accessToken);
  }

  logOutUser() {
    this.userStore.isLoggedIn = false;
    this.userStore.accessToken = '';
    this.setUser(
      {
        id: null,
        first_name: null,
        last_name: null,
        email: null,
        iat: null,
        exp: null,
      },
      false,
      ''
    );
  }
}
