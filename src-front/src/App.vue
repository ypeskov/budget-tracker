<script setup>
import { onBeforeMount } from 'vue';
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { useUserStore } from './stores/user';
import { UserService } from './services/users';

const router = useRouter();
const t = useI18n().t;
const { locale } = useI18n();

const userStore = useUserStore();
const userService = new UserService(userStore);

onBeforeMount(async () => {
  let isLoggedIn, accessToken, localStorageUser;
  try {
    localStorageUser = JSON.parse(localStorage.getItem('user'));
    isLoggedIn = JSON.parse(localStorage.getItem('isLoggedIn'));
    accessToken = localStorage.getItem('accessToken');
  } catch (e) {
    userService.logOutUser();
  }

  if (isLoggedIn) {
    locale.value = localStorageUser.settings.language;
    userService.setUser(localStorageUser, isLoggedIn, accessToken);
  }
});

const goToSettings = () => {
  router.push({ name: 'settings' });
};
</script>

<template>
  <div class="container">
    <div class="row ">
      <div class="col header-row">
        <div>{{ $t('message.anotherBudgeter') }}</div>
        <div class="settings-icon" @click="goToSettings">
          <img src="/images/icons/settings.svg" :alt="t('message.settings')">
        </div>
      </div>

    </div>
    <header>
      <div class="row nav-row">
        <div class="col">
          <nav>
              <span>
                <RouterLink :to="{ name: 'home' }">{{ $t('menu.home') }}</RouterLink>
              </span>
            <span v-if="userStore.isLoggedIn">
                <RouterLink :to="{ name: 'accounts' }">{{ $t('menu.accounts') }}</RouterLink>
              </span>
            <span v-if="userStore.isLoggedIn">
                <RouterLink :to="{ name: 'transactions' }">{{ $t('menu.transactions') }}</RouterLink>
              </span>
            <span v-if="!userStore.isLoggedIn">
                <RouterLink :to="{ name: 'login' }">{{ $t('menu.login') }}</RouterLink>
                <RouterLink :to="{ name: 'register' }">{{ $t('menu.register') }}</RouterLink>
              </span>
            <span v-else>
                <RouterLink :to="{ name: 'logout' }">{{ $t('menu.logout') }}</RouterLink>
              </span>
          </nav>
        </div>
      </div>
      <div class="row">
        <div class="col">

        </div>
      </div>
    </header>
  </div>
  <RouterView />
</template>

<style scoped>
nav a {
  margin: 0 0.2rem;
}

.nav-row {
  margin-bottom: 0.5rem;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.settings-icon img {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.settings-icon img:hover {
  transform: scale(1.1);
}
</style>
