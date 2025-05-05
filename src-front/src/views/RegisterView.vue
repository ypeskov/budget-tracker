<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { Services } from '@/services/servicesConfig';
import { GoogleLogin } from 'vue3-google-login';

const router = useRouter();
const { t }  = useI18n();

const firstName        = ref('');
const lastName         = ref('');
const registerEmail    = ref('');
const registerPassword = ref('');
const errorMessage     = ref('');
const showSuccess      = ref(false);

const emailRef = ref(null);
onMounted(() => emailRef.value?.focus());

async function submitRegistration() {
  errorMessage.value = '';
  try {
    await Services.userService.registerUser(
      registerEmail.value,
      registerPassword.value,
      firstName.value,
      lastName.value
    );
    showSuccess.value = true;
  } catch (err) {
    errorMessage.value = `Registration failed: ${err.message}`;
  }
}

const callback = async (response) => {
  errorMessage.value = '';
  try {
    await Services.userService.oauthLogin(response.credential);
    await router.push({ name: 'accounts' });
  } catch (err) {
    errorMessage.value = `Registration failed: ${err.message}`;
  }
};
</script>

<template>
  <div class="login-page">
    <div class="box">

      <div class="left">
        <form
          v-if="!showSuccess"
          @submit.prevent="submitRegistration"
          autocomplete="on"
        >
          <h1>Orgfin.run</h1>
          <small>{{ t('message.registerAccount') }}</small>

          <div class="field">
            <span><i class="fa fa-user"></i></span>
            <input
              type="text"
              v-model="firstName"
              :placeholder="t('message.firstName')"
            />
          </div>

          <div class="field">
            <span><i class="fa fa-user"></i></span>
            <input
              type="text"
              v-model="lastName"
              :placeholder="t('message.lastName')"
            />
          </div>

          <div class="field">
            <span><i class="fa fa-envelope"></i></span>
            <input
              ref="emailRef"
              type="email"
              v-model="registerEmail"
              :placeholder="t('message.enterEmail')"
              required
            />
          </div>

          <div class="field">
            <span><i class="fa fa-lock"></i></span>
            <input
              type="password"
              v-model="registerPassword"
              :placeholder="t('message.enterPassword')"
              required
            />
          </div>

          <button type="submit">{{ t('menu.register') }}</button>

          <div class="oauth-container">
            <GoogleLogin :callback="callback" />
          </div>

          <div v-if="errorMessage" class="alert" style="margin-top:20px">
            {{ errorMessage }}
          </div>
        </form>

        <div v-else>
          <h1>{{ t('message.success') }}</h1>
          <p>{{ t('message.checkEmailForVerification') }}</p>
          <button @click="router.push({ name: 'login' })">
            {{ t('menu.login') }}
          </button>
        </div>
      </div>

      <div class="right">
        <h2>{{ t('message.alreadyRegistered') }}</h2>
        <p>{{ t('message.justLoginBelow') }}</p>
        <RouterLink class="register-link" :to="{ name: 'login' }">
          {{ t('menu.login') }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped src="@/assets/auth.css"></style>
