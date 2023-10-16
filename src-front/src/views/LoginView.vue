<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { Services } from '../services/servicesConfig';

let loginEmail = ref('');
let loginPassword = ref('');

const router = useRouter();

function updateEmail(event) {
  loginEmail.value = event.target.value;
}

async function submitLogin() {
  await Services.userService.loginUser(loginEmail.value, loginPassword.value);
  loginEmail.value = '';
  loginPassword.value = '';
  router.push('/');
}
</script>

<template>
  <div class="container">
    <main>
      <form @submit.prevent="submitLogin" autocomplete="on">
        <div class="row">
          <div class="col">
            <input type="email" :value="loginEmail" @change="updateEmail" />
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
