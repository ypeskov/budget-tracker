<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useI18n } from 'vue-i18n';

const router = useRouter();
const userStore = useUserStore();
const { t } = useI18n();

if (userStore.user.email) {
  router.push({ name: 'accounts' });
}

const features = [
  {
    icon: 'fa fa-chart-line',
    titleKey: 'home.features.analytics.title',
    descKey: 'home.features.analytics.desc',
  },
  {
    icon: 'fa fa-wallet',
    titleKey: 'home.features.budgeting.title',
    descKey: 'home.features.budgeting.desc',
  },
  {
    icon: 'fa fa-mobile-alt',
    titleKey: 'home.features.mobile.title',
    descKey: 'home.features.mobile.desc',
  },
];
</script>

<template>
  <div class="home-page">
    <header class="nav">
      <div class="logo">Orgfin.run</div>
      <nav>
        <RouterLink
          v-if="!userStore.user.id"
          :to="{ name: 'login' }"
          class="btn primary"
        >
          {{ t('menu.login') }}
        </RouterLink>
        <RouterLink
          v-if="!userStore.user.id"
          :to="{ name: 'register' }"
          class="btn outline"
        >
          {{ t('menu.register') }}
        </RouterLink>
        <RouterLink
          v-else
          :to="{ name: 'accounts' }"
          class="btn primary"
        >
          {{ t('menu.dashboard') }}
        </RouterLink>
      </nav>
    </header>

    <section class="hero">
      <div class="hero-content">
        <h1>{{ t('home.heroTitle') }}</h1>
        <p>{{ t('home.heroSubtitle') }}</p>
        <RouterLink
          :to="{ name: userStore.user.id ? 'accounts' : 'login' }"
          class="btn primary cta"
        >
          {{ userStore.user.id ? t('menu.goToDashboard') : t('menu.getStartedFree') }}
        </RouterLink>
      </div>
      <div class="hero-img">
        <img src="/public/images/dashboard.png" alt="Finance dashboard illustration" />
      </div>
    </section>

    <section class="features">
      <div
        class="feature-card"
        v-for="(feature, index) in features"
        :key="index"
      >
        <div class="icon"><i :class="feature.icon"></i></div>
        <h3>{{ t(feature.titleKey) }}</h3>
        <p>{{ t(feature.descKey) }}</p>
      </div>
    </section>

    <footer class="footer">© {{ new Date().getFullYear() }} Orgfin.run</footer>
  </div>
</template>
