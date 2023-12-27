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
  <div class="container mt-5">
    <main>
      <form @submit.prevent="submitLogin" autocomplete="on">
        <div class="mb-3">
          <label for="emailInput" class="form-label">
            Email Address <span class="text-danger">*</span> <!-- Red asterisk for required field -->
          </label>
          <input type="email" class="form-control" id="emailInput" :value="loginEmail" @change="updateEmail"
            ref="emailInputRef" placeholder="Enter Email" required /> <!-- 'required' attribute added -->
        </div>
        <div class="mb-3">
          <label for="passwordInput" class="form-label">
            Password <span class="text-danger">*</span> <!-- Red asterisk for required field -->
          </label>
          <input type="password" class="form-control" id="passwordInput" v-model="loginPassword"
            placeholder="Enter Password" required /> <!-- 'required' attribute added -->
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </main>
  </div>
</template>

