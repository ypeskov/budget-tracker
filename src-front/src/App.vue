<script setup>
import { onBeforeMount } from 'vue';
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { useUserStore } from './stores/user';
import { UserService } from './services/users';

const router = useRouter();
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
        <div v-if="userStore.isLoggedIn" class="settings-icon" @click="goToSettings">
          <img src="/images/icons/settings-icon.svg"
               :title="$t('message.settings')"
               :alt="$t('message.settings')">
        </div>
      </div>

    </div>
    <header>
      <div class="row nav-row">
        <div class="col">
          <nav>
            <span v-if="!userStore.isLoggedIn">
              <RouterLink :to="{ name: 'home' }">
                <img src="/images/icons/home-icon.svg"
                     class="main-menu-icon"
                     :title="$t('menu.home')"
                     :alt="$t('menu.home')">
              </RouterLink>
            </span>
            <span v-if="userStore.isLoggedIn">
              <RouterLink :to="{ name: 'accounts' }">
                <img src="/images/icons/accounts-icon.svg"
                     class="main-menu-icon"
                     :title="$t('menu.accounts')"
                     :alt="$t('menu.accounts')">
              </RouterLink>
            </span>
            <span v-if="userStore.isLoggedIn">
              <RouterLink :to="{ name: 'transactions' }">
                <img src="/images/icons/transactions-icon.svg"
                     class="main-menu-icon"
                     :title="$t('menu.transactions')"
                     :alt="$t('menu.accounts')">
              </RouterLink>
            </span>
            <span v-if="userStore.isLoggedIn">
              <RouterLink :to="{ name: 'reports' }">
                <img src="/images/icons/reports-icon.svg"
                     class="main-menu-icon"
                     :title="$t('menu.reports')"
                     :alt="$t('menu.reports')">
              </RouterLink>
            </span>
            <span v-if="!userStore.isLoggedIn">
              <RouterLink :to="{ name: 'login' }">
                <img src="/images/icons/enter-icon.svg"
                     class="main-menu-icon"
                     :title="$t('menu.login')"
                     :alt="$t('menu.login')">
              </RouterLink>
              <RouterLink :to="{ name: 'register' }">
                <img src="/images/icons/register-icon.svg"
                     class="main-menu-icon"
                     :title="$t('menu.register')"
                     :alt="$t('menu.register')">
              </RouterLink>
            </span>
            <span v-else>
                <RouterLink :to="{ name: 'logout' }">
                  <img src="/images/icons/exit-icon.svg"
                       class="main-menu-icon"
                       :title="$t('menu.logout')"
                       :alt="$t('menu.logout')">
                </RouterLink>
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
