import { HttpError } from '../errors/HttpError';
import { request } from './requests';

export class UserService {
  userStore;

  constructor(userStore) {
    this.userStore = userStore;
  }

  injectServices(services = {}) {
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
      const data = await request(
        loginPath,
        {
          method: 'POST',
          body: JSON.stringify(requestBody),
        },
        { userService: this },
      );
      if (data.access_token) {
        this.userStore.accessToken = data.access_token;
        await this.getUserProfile(this.userStore.accessToken);
        this.accountsService.getAllUserAccounts();
      } else {
        console.log('Something went wrong!');
      }
    } catch (e) {
      if (e instanceof HttpError && e.statusCode === 401) {
        console.log('Wrong email or password!');
      }
      throw e;
    }
  }

  async getUserProfile(accessToken) {
    try {
      const profileEndpoint = '/auth/profile/';
      const userProfile = await request(profileEndpoint, {}, { userService: this });
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
    this.userStore.settings = Object.assign(this.userStore.settings, userProfile.settings);

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
      '',
    );
  }

  async registerUser(email, password, firstName, lastName) {
    const registerPath = '/auth/register/';
    const requestBody = {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
    };
    try {
      const data = await request(
        registerPath,
        {
          method: 'POST',
          body: JSON.stringify(requestBody),
        },
        { userService: this },
      );
      console.log('Registration successful');
    } catch (e) {
      if (e instanceof HttpError) {
        console.error('Registration error:', e.message);
      } else {
        console.error('Unexpected error:', e);
      }
      throw e;
    }
  }
}
