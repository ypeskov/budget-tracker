<script setup>
import { onBeforeMount, onBeforeUnmount, onMounted, computed } from 'vue';
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { useUserStore } from '@/stores/user';
import { UserService }   from '@/services/users';
import { TransactionsService } from '@/services/transactions';

const router = useRouter();
const route  = useRoute();
const { locale, t } = useI18n();

const userStore = useUserStore();
const userService = new UserService(userStore);
const transactionsService = new TransactionsService(userStore);

const publicPages = ['login', 'register', 'home'];
const hideHeader = computed(() => publicPages.includes(route.name));

onMounted(() => {
  if (userStore.isLoggedIn) userStore.startTimer();
});
onBeforeUnmount(() => {
  userStore.stopTimer();
});

onBeforeMount(async () => {
  let isLoggedIn, accessToken, localStorageUser;
  try {
    localStorageUser = JSON.parse(localStorage.getItem('user'));
    isLoggedIn       = JSON.parse(localStorage.getItem('isLoggedIn'));
    accessToken      = localStorage.getItem('accessToken');
  } catch {
    await userService.logOutUser();
  }
  if (isLoggedIn) {
    locale.value = localStorageUser.settings.language;
    userService.setUser(localStorageUser, isLoggedIn, accessToken);
  }
});

const goToSettings = () => router.push({ name: 'settings' });
</script>

<template>
  <div v-if="!hideHeader" class="container">
    <div class="row">
      <div class="col header-row">
        <div>{{ t('message.anotherBudgeter') }}</div>
        <div>{{ userStore.timeLeft }}</div>
        <div
          v-if="userStore.isLoggedIn"
          class="settings-icon"
          @click="goToSettings"
        >
          <img
            src="/images/icons/settings-icon.svg"
            :title="t('message.settings')"
            :alt="t('message.settings')"
          />
        </div>
      </div>
    </div>

    <header>
      <div class="row nav-row">
        <div class="col">
          <nav>
            <span v-if="!userStore.isLoggedIn">
              <RouterLink :to="{ name: 'home' }">
                <img
                  src="/images/icons/home-icon.svg"
                  class="main-menu-icon"
                  :title="t('menu.home')"
                  :alt="t('menu.home')"
                />
              </RouterLink>
              <RouterLink :to="{ name: 'login' }">
                <img
                  src="/images/icons/enter-icon.svg"
                  class="main-menu-icon"
                  :title="t('menu.login')"
                  :alt="t('menu.login')"
                />
              </RouterLink>
              <RouterLink :to="{ name: 'register' }">
                <img
                  src="/images/icons/register-icon.svg"
                  class="main-menu-icon"
                  :title="t('menu.register')"
                  :alt="t('menu.register')"
                />
              </RouterLink>
            </span>

            <template v-else>
              <RouterLink :to="{ name: 'accounts' }">
                <img
                  src="/images/icons/accounts-icon.svg"
                  class="main-menu-icon"
                  :title="t('menu.accounts')"
                  :alt="t('menu.accounts')"
                />
              </RouterLink>
              <RouterLink :to="{ name: 'transactions' }">
                <img
                  src="/images/icons/transactions-icon.svg"
                  class="main-menu-icon"
                  :title="t('menu.transactions')"
                  :alt="t('menu.transactions')"
                />
              </RouterLink>
              <RouterLink :to="{ name: 'reports' }">
                <img
                  src="/images/icons/reports-icon.svg"
                  class="main-menu-icon"
                  :title="t('menu.reports')"
                  :alt="t('menu.reports')"
                />
              </RouterLink>
              <RouterLink :to="{ name: 'budgets' }">
                <img
                  src="/images/icons/budgets-icon.svg"
                  class="main-menu-icon"
                  :title="t('menu.budgets')"
                  :alt="t('menu.budgets')"
                />
              </RouterLink>
              <RouterLink :to="{ name: 'logout' }">
                <img
                  src="/images/icons/exit-icon.svg"
                  class="main-menu-icon"
                  :title="t('menu.logout')"
                  :alt="t('menu.logout')"
                />
              </RouterLink>
            </template>
          </nav>
        </div>
      </div>
    </header>
  </div>

  <RouterView />
</template>

<style src="@/assets/style.css"></style>
