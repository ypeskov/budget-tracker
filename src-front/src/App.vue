<script setup>
import { onBeforeMount, onBeforeUnmount, onMounted, computed } from 'vue';
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { useUserStore } from '@/stores/user';
import { UserService }   from '@/services/users';

const router = useRouter();
const route  = useRoute();
const { locale, t } = useI18n();

const userStore   = useUserStore();
const userService = new UserService(userStore);

const publicPages = ['login', 'register', 'home'];
const hideHeader  = computed(() => publicPages.includes(route.name));

onBeforeMount(() => {
  try {
    const usr = JSON.parse(localStorage.getItem('user'));
    const ok  = JSON.parse(localStorage.getItem('isLoggedIn'));
    const tok = localStorage.getItem('accessToken');
    if (ok) {
      locale.value = usr.settings.language;
      userService.setUser(usr, ok, tok);
    }
  } catch { userService.logOutUser(); }
});

onMounted      (() => { if (userStore.isLoggedIn) userStore.startTimer(); });
onBeforeUnmount(() =>   userStore.stopTimer());

const goToSettings = () => router.push({ name: 'settings' });
</script>

<template>
  <header v-if="!hideHeader" class="navbar">
    <div class="container nav-inner">

      <nav class="nav-left">
        <template v-if="!userStore.isLoggedIn">
          <RouterLink :to="{ name: 'home'     }" class="btn btn-icon" :title="t('menu.home')">
            <i class="fa-solid fa-house"></i>
          </RouterLink>
          <RouterLink :to="{ name: 'login'    }" class="btn btn-icon" :title="t('menu.login')">
            <i class="fa-solid fa-right-to-bracket"></i>
          </RouterLink>
          <RouterLink :to="{ name: 'register' }" class="btn btn-icon" :title="t('menu.register')">
            <i class="fa-solid fa-user-plus"></i>
          </RouterLink>
        </template>

        <template v-else>
          <RouterLink :to="{ name: 'accounts'     }" class="btn btn-icon" :title="t('menu.accounts')">
            <i class="fa-solid fa-wallet"></i>
          </RouterLink>
          <RouterLink :to="{ name: 'transactions' }" class="btn btn-icon" :title="t('menu.transactions')">
            <i class="fa-solid fa-right-left"></i>
          </RouterLink>
          <RouterLink :to="{ name: 'reports'      }" class="btn btn-icon" :title="t('menu.reports')">
            <i class="fa-solid fa-chart-pie"></i>
          </RouterLink>
          <RouterLink :to="{ name: 'budgets'      }" class="btn btn-icon" :title="t('menu.budgets')">
            <i class="fa-solid fa-list-check"></i>
          </RouterLink>
          <RouterLink :to="{ name: 'planning'     }" class="btn btn-icon" :title="t('menu.planning')">
            <i class="fa-solid fa-calendar-days"></i>
          </RouterLink>
          <RouterLink :to="{ name: 'logout'       }" class="btn btn-icon" :title="t('menu.logout')">
            <i class="fa-solid fa-right-from-bracket"></i>
          </RouterLink>
        </template>
      </nav>

      <div class="nav-right" v-if="userStore.isLoggedIn">
        <span class="time">{{ userStore.timeLeft }}</span>

        <button class="btn btn-icon btn-outline-primary"
                @click="goToSettings"
                :title="t('message.settings')">
          <i class="fa-solid fa-gear"></i>
        </button>
      </div>
    </div>
  </header>

  <RouterView />
</template>

<style src="@/assets/style.css"></style>
