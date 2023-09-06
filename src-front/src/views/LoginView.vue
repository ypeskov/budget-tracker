<script setup>
import { ref } from 'vue';
import {useRouter} from 'vue-router';

import { useUserStore } from '../stores/user';

let loginEmail = ref('');
let loginPassword = ref('');
const userStore = useUserStore();
const router = useRouter();

function updateEmail(event) {
  loginEmail.value = event.target.value;
}

async function submitLogin() {
  await userStore.loginUser(loginEmail.value, loginPassword.value);
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
