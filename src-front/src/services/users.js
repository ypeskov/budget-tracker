import { useUserStore } from "../stores/user";

export class UserService {
  userStore;
  
  constructor() {
    this.userStore = useUserStore();
  }

  async loginUser(loginEmail, password) {
    const loginPath = 'http://localhost:9000/auth/login';
    const requestHeaders = {
      'Content-Type': 'application/json',
    };
    const requestBody = {
      email: loginEmail,
      password,
    };
    try {
      const response = await fetch(loginPath, {
        method: 'POST',
        headers: requestHeaders,
        body: JSON.stringify(requestBody),
      });
  
      const data = await response.json();
      if (data.access_token) {
        this.userStore.accessToken = data.access_token;
        this.getUserProfile(this.userStore.accessToken);
      } else {
        alert('Something went wrong!');
      }
    } catch (e) {
      console.log(e);
    }
  }
  
  async getUserProfile(accessToken) {
    try {
      const profileEndpoint = 'http://localhost:9000/auth/profile';
      const response = await fetch(profileEndpoint, {
        headers: {
          'auth-token': accessToken,
          'Content-Type': 'application/json',
        },
      });
      const userProfile = await response.json();
      this.setUser(userProfile, true, accessToken);
    } catch (e) {
      console.log(e);
    }
  }
  
  setUser(userProfile, isLoggedIn=false, accessToken='') {
    this.userStore.user.id = userProfile.id;
    this.userStore.user.firstName = userProfile.firstName;
    this.userStore.user.lastName = userProfile.lastName;
    this.userStore.user.email = userProfile.email;
    this.userStore.user.iat = userProfile.iat;
    this.userStore.user.exp = userProfile.exp;
  
    this.userStore.isLoggedIn = isLoggedIn;
    this.userStore.accessToken = accessToken;

    localStorage.setItem('user', JSON.stringify(this.userStore.user));
    localStorage.setItem('isLoggedIn', this.userStore.isLoggedIn);
    localStorage.setItem('accessToken', this.userStore.accessToken);
  }
  
  logOutUser() {
    this.userStore.isLoggedIn = false;
    this.userStore.accessToken = '';
    this.setUser({
        id: null,
        firstName: null,
        lastName: null,
        email: null,
        iat: null,
        exp: null,
      },
      false,
      ''
    );
  }
}