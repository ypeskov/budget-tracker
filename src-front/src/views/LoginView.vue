<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { Services } from '../services/servicesConfig';
import { HttpError } from '../errors/HttpError';
import { useUserStore } from '../stores/user';
import { GoogleLogin } from 'vue3-google-login';

const userStore = useUserStore();

let loginEmail = ref('');
let loginPassword = ref('');

const router = useRouter();
const { t } = useI18n();
const { locale } = useI18n();

function updateEmail(event) {
  loginEmail.value = event.target.value;
}

async function submitLogin() {
  try {
    await Services.userService.loginUser(loginEmail.value, loginPassword.value);
    await afterLogin();
  } catch (error) {
    processError(error);
  }
}

const afterLogin = async () => {
  loginEmail.value = '';
  loginPassword.value = '';
  locale.value = userStore.settings.language;
  await router.push({ name: 'accounts' });
};

const emailInputRef = ref(null);
onMounted(() => {
  if (emailInputRef.value) {
    emailInputRef.value.focus();
  }
});

const processError = function (error) {
  if (error instanceof HttpError && error.statusCode === 401) {
    if (error.message === 'User not activated') {
      alert(t('message.userNotActivated'));
    } else {
      alert(t('message.invalidCredentials'));
    }
  } else {
    console.log('Something went wrong');
  }
};

const callback = async (response) => {
  try {
    await Services.userService.oauthLogin(response.credential);
    await afterLogin();
  } catch (error) {
    processError(error);
  }
};
</script>

<template>
  <div class="container mt-5">
    <main>
      <div class="row">
        <div class="col">
          <form
            @submit.prevent="submitLogin"
            autocomplete="on">
            <div class="mb-3">
              <label
                for="emailInput"
                class="form-label">
                {{ $t('message.emailAddress') }}
                <span class="text-danger">*</span>
              </label>
              <input
                type="email"
                class="form-control"
                id="emailInput"
                :value="loginEmail"
                @change="updateEmail"
                ref="emailInputRef"
                :placeholder="t('message.enterEmail')"
                required />
            </div>
            <div class="mb-3">
              <label
                for="passwordInput"
                class="form-label">
                Password
                <span class="text-danger">*</span>
              </label>
              <input
                type="password"
                class="form-control"
                id="passwordInput"
                v-model="loginPassword"
                :placeholder="t('message.enterPassword')"
                required />
            </div>
            <button
              type="submit"
              class="btn btn-primary">
              {{ $t('menu.login') }}
            </button>
          </form>
        </div>
      </div>

      <div class="row">
        <div class="col-3 mt-4">
          <GoogleLogin
            :callback="callback"
            opt />
        </div>
      </div>
    </main>
  </div>
</template>
