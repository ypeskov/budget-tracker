<script setup>
import { ref } from 'vue';
import { useBudgetStore } from '../stores/budget';

const loginEmail = ref('');
const loginPassword = ref('');

const loginPath = 'http://localhost:9000/auth/login';
async function submitLogin() {
  const requestBody = {
    email: loginEmail.value,
    password: loginPassword.value
  };
  const response = await fetch(loginPath, {
    'method': 'POST',
    'headers': {
      'Content-Type': 'application/json'
    },
    'body': JSON.stringify(requestBody)
  });

  const data = await response.json();
  console.log(data);
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
