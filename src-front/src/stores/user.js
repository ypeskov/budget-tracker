import { ref, reactive, toRefs } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const userTemplate = {
    id: null,
    firstName: null,
    lastName: null,
    email: null,
    iat: null,
    exp: null
  };
  const user = reactive(userTemplate);
  
  const authToken = ref(null);
  

  async function loginUser(loginEmail, password) {
    const loginPath = 'http://localhost:9000/auth/login'
    const requestHeaders = {
      'Content-Type': 'application/json'
    }
    const requestBody = {
      email: loginEmail,
      password
    }
    try {
      const response = await fetch(loginPath, {
        method: 'POST',
        headers: requestHeaders,
        body: JSON.stringify(requestBody)
      })

      const data = await response.json()
      if (data.access_token) {
        user.email = requestBody.email;
        authToken.value = data.access_token;
        getUserProfile(authToken.value);
      } else {
        alert('Ahctung!')
      }
    } catch (e) {
      console.log(e);
    }
  }

  async function getUserProfile(authToken) {
    try {
      const profileEndpoint = 'http://localhost:9000/auth/profile'
      const response = await fetch(profileEndpoint, {
        headers: {
          'auth-token': authToken,
          'Content-Type': 'application/json'
        }
      })
      const userProfile = await response.json();
      setUser(userProfile);
    } catch (e) {
      console.log(e);
    }
  }

  function setUser(userProfile) {
    user.id = userProfile.id;
    user.firstName = userProfile.firstName;
    user.lastName = userProfile.lastName;
    user.email = userProfile.email;
    user.iat = userProfile.iat;
    user.exp = userProfile.exp;
  }

  return { user, loginUser, getUserProfile, authToken }
})
