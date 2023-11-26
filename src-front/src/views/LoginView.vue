<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { Services } from '../services/servicesConfig';
import { HttpError } from '../errors/HttpError';

let loginEmail = ref('');
let loginPassword = ref('');

const router = useRouter();

function updateEmail(event) {
  loginEmail.value = event.target.value;
}

async function submitLogin() {
  try {
    await Services.userService.loginUser(loginEmail.value, loginPassword.value);
    loginEmail.value = '';
    loginPassword.value = '';
    router.push('/');
  } catch (error) {
    if (error instanceof HttpError && error.statusCode === 401) {
      console.log(error.message);
      alert('Wrong email or password');
      return;
    } else {
      console.log('Something went wrong');
      console.log(error);
    }
  }
}

const emailInputRef = ref(null);
onMounted(() => {
  if (emailInputRef.value) {
    emailInputRef.value.focus();
  }
});
</script>

<template>
  <div class="container">
    <main>
      <form @submit.prevent="submitLogin" autocomplete="on">
        <div class="row">
          <div class="col">
            <input type="email" :value="loginEmail" @change="updateEmail" ref="emailInputRef" />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <input type="password" v-model="loginPassword" />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <button type="submit">Login</button>
          </div>
        </div>
      </form>
    </main>
  </div>
</template>
