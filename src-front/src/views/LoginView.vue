<script setup>
import { ref } from 'vue';
import {useRouter} from 'vue-router';

import { useUserStore } from '../stores/user';

const loginEmail = ref('');
const loginPassword = ref('');
const userStore = useUserStore();
const router = useRouter();


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
      <form @submit.prevent="submitLogin">
        <div class="row">
          <div class="col">
            <input type="email" v-model="loginEmail" />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <input type="password" v-model="loginPassword" />
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
