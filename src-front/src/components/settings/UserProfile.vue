<script setup>
import { ref } from 'vue';

import LanguageSelector     from './LanguageSelector.vue';
import BaseCurrencyManager  from './BaseCurrencyManager.vue';

const tab = ref('lang');   // 'lang' | 'curr'
</script>

<template>
  <div class="profile-wrapper">

    <!-- ── локальное меню профиля ── -->
    <nav class="profile-tabs">
      <button class="btn outline"
              :class="{ active: tab === 'lang' }"
              @click="tab = 'lang'">
        <i class="fa-solid fa-language"></i>
        {{ $t('buttons.language') }}
      </button>

      <button class="btn outline"
              :class="{ active: tab === 'curr' }"
              @click="tab = 'curr'">
        <i class="fa-solid fa-money-bill-wave"></i>
        {{ $t('buttons.baseCurrency') }}
      </button>
    </nav>

    <!-- ── активная секция ── -->
    <div class="profile-body">
      <LanguageSelector    v-if="tab === 'lang'"  />
      <BaseCurrencyManager v-else                />
    </div>
  </div>
</template>

<style scoped>
.profile-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.profile-tabs {
  display: flex;
  gap: 16px;
}
.profile-tabs .btn {
  display: flex;
  align-items: center;
  gap: 8px;
}
.profile-tabs .btn.active,
.profile-tabs .btn.active:hover {
  background: #1e90ff;
  color: #fff;
}
.profile-body { width: 100%; }
</style>
