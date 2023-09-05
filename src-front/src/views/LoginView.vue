<script setup>
import { ref } from 'vue';
import { useUserStore } from '../stores/user';

const loginEmail = ref('');
const loginPassword = ref('');
const userStore = useUserStore();

async function submitLogin() {
  await userStore.loginUser(loginEmail.value, loginPassword.value);
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
