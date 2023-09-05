<script setup>
import { ref } from 'vue';
import { useUserStore } from '../stores/user';

const loginEmail = ref('');
const loginPassword = ref('');
const userStore = useUserStore();

async function submitLogin() {
  const loginPath = 'http://localhost:9000/auth/login';
  const requestBody = {
    email: loginEmail.value,
    password: loginPassword.value
  };
  try {
    const response = await fetch(loginPath, {
      'method': 'POST',
      'headers': {
        'Content-Type': 'application/json'
      },
      'body': JSON.stringify(requestBody)
    });

    const data = await response.json();
    if (data.access_token) {
      userStore.email = requestBody.email;
      userStore.accessToken = data.access_token;

      const profileEndpoint = 'http://localhost:9000/auth/profile';
      const response = await fetch(profileEndpoint, {
        'headers': {
          'auth-token': userStore.accessToken,
          'Content-Type': 'application/json'
        }
      });
      const profile = await response.json();
      userStore.id = profile.id;
      userStore.firstName = profile.firstName;
      userStore.lastName = profile.lastName;
      userStore.iat = profile.iat;
      userStore.exp = profile.exp;
    } else {
      alert('Ahctung!');
    }
  }
  catch (e) {
    console.log(e);
  }
}
</script>

<template>
  <div class="container">
    <main>
      <form @submit.prevent="submitLogin">
        <div class="row">
          <div class="col">
            <input type="text" v-model="loginEmail" />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <input type="text" v-model="loginPassword" />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <button>Login</button>
          </div>
        </div>
      </form>
    </main>
  </div>
</template>
