import { ref, reactive, toRefs } from 'vue';
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {
  const userTemplate = {
    id: null,
    firstName: null,
    lastName: null,
    email: null,
    iat: null,
    exp: null,
  };
  const user = reactive(userTemplate);

  const accessToken = ref(null);
  const isLoggedIn = ref(false);

  async function loginUser(loginEmail, password) {
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
        user.email = requestBody.email;
        accessToken.value = data.access_token;
        getUserProfile(accessToken.value);
      } else {
        alert('Ahctung!');
      }
    } catch (e) {
      console.log(e);
    }
  }

  async function getUserProfile(accessToken) {
    try {
      const profileEndpoint = 'http://localhost:9000/auth/profile';
      const response = await fetch(profileEndpoint, {
        headers: {
          'auth-token': accessToken,
          'Content-Type': 'application/json',
        },
      });
      const userProfile = await response.json();
      setUser(userProfile, true, accessToken);
    } catch (e) {
      console.log(e);
    }
  }

  function setUser(userProfile, externalIsLoggedIn=false, externalAccessToken='') {
    user.id = userProfile.id;
    user.firstName = userProfile.firstName;
    user.lastName = userProfile.lastName;
    user.email = userProfile.email;
    user.iat = userProfile.iat;
    user.exp = userProfile.exp;

    isLoggedIn.value = externalIsLoggedIn;
    accessToken.value = externalAccessToken
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('isLoggedIn', isLoggedIn.value);
    localStorage.setItem('accessToken', accessToken.value);
  }

  function logOutUser() {
    isLoggedIn.value = false;
    accessToken.value = '';
    setUser({
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

  return {
    user,
    loginUser,
    getUserProfile,
    setUser,
    accessToken,
    isLoggedIn,
    logOutUser,
  };
});
