<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { Services } from '../services/servicesConfig';
import { HttpError } from '../errors/HttpError';

let loginEmail = ref('');
let loginPassword = ref('');

const router = useRouter();
const { t } = useI18n();

function updateEmail(event) {
  loginEmail.value = event.target.value;
}

async function submitLogin() {
  try {
    await Services.userService.loginUser(loginEmail.value, loginPassword.value);
    loginEmail.value = '';
    loginPassword.value = '';
    await router.push('/');
  } catch (error) {
    if (error instanceof HttpError && error.statusCode === 401) {
      console.log(error.message);
      alert(t('message.invalidCredentials'));
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
            {{ $t('message.emailAddress') }} <span class="text-danger">*</span>
          </label>
          <input type="email" class="form-control" id="emailInput" :value="loginEmail" @change="updateEmail"
            ref="emailInputRef" :placeholder="t('message.enterEmail')" required />
        </div>
        <div class="mb-3">
          <label for="passwordInput" class="form-label">
            Password <span class="text-danger">*</span>
          </label>
          <input type="password" class="form-control" id="passwordInput" v-model="loginPassword"
            :placeholder="t('message.enterPassword')" required />
        </div>
        <button type="submit" class="btn btn-primary">{{$t('menu.login')}}</button>
      </form>
    </main>
  </div>
</template>

