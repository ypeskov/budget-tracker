<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { Services } from '@/services/servicesConfig';
import { HttpError } from '@/errors/HttpError';
import { useUserStore } from '@/stores/user';
import { GoogleLogin } from 'vue3-google-login';

const userStore = useUserStore();
const router    = useRouter();
const { t, locale } = useI18n();

const email      = ref('');
const password   = ref('');
const loginError = ref('');
const emailRef   = ref(null);

onMounted(() => emailRef.value?.focus());

async function submitLogin() {
  loginError.value = '';
  try {
    await Services.userService.loginUser(email.value, password.value);
    await afterLogin();
  } catch (err) {
    processError(err);
  }
}

async function afterLogin() {
  email.value    = '';
  password.value = '';
  locale.value   = userStore.settings.language;
  await router.push({ name: 'accounts' });
}

function processError(err) {
  if (err instanceof HttpError && err.statusCode === 401) {
    loginError.value = err.message === 'User not activated'
      ? t('message.userNotActivated')
      : t('message.invalidCredentials');
  } else {
    console.error(err);
    loginError.value = t('message.unexpectedError');
  }
}

const callback = async (response) => {
  try {
    await Services.userService.oauthLogin(response.credential);
    await afterLogin();
  } catch (err) {
    processError(err);
  }
};
</script>

<template>
  <div class="login-page">
    <div class="box">
      <form class="left" @submit.prevent="submitLogin" autocomplete="on">
        <h1>Orgfin.run</h1>
        <small>{{ t('message.loginToAccount') }}</small>

        <div class="field">
          <span><i class="fa fa-envelope"></i></span>
          <input
            ref="emailRef"
            v-model="email"
            type="email"
            :placeholder="t('message.enterEmail')"
            required
          />
        </div>

        <div class="field">
          <span><i class="fa fa-lock"></i></span>
          <input
            v-model="password"
            type="password"
            :placeholder="t('message.enterPassword')"
            required
          />
        </div>

        <button type="submit">{{ t('menu.login') }}</button>

        <div class="oauth-container">
          <GoogleLogin :callback="callback" />
        </div>

        <div v-if="loginError" class="alert">
          <strong>{{ t('message.error') }}</strong> {{ loginError }}
        </div>
      </form>

      <div class="right">
        <h2>{{ t('message.noAccount') }}</h2>
        <p>{{ t('message.registerInvite') }}</p>
        <RouterLink class="register-link" :to="{ name: 'register' }">
          {{ t('menu.register') }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped src="@/assets/auth.css"></style>
