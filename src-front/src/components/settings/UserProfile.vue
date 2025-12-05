<script setup>
import { ref } from 'vue';

import LanguageSelector     from './LanguageSelector.vue';
import BaseCurrencyManager  from './BaseCurrencyManager.vue';
import ChangePassword       from './ChangePassword.vue';

const tab = ref('lang');   // 'lang' | 'curr' | 'password'
</script>

<template>
  <div class="profile-wrapper">

    <!-- Profile local menu -->
    <nav class="profile-tabs">
      <button class="btn btn-outline-primary"
              :class="{ active: tab === 'lang' }"
              @click="tab = 'lang'">
        <i class="fa-solid fa-language"></i>
        {{ $t('buttons.language') }}
      </button>

      <button class="btn btn-outline-primary"
              :class="{ active: tab === 'curr' }"
              @click="tab = 'curr'">
        <i class="fa-solid fa-money-bill-wave"></i>
        {{ $t('buttons.baseCurrency') }}
      </button>

      <button class="btn btn-outline-primary"
              :class="{ active: tab === 'password' }"
              @click="tab = 'password'">
        <i class="fa-solid fa-lock"></i>
        {{ $t('buttons.changePassword') }}
      </button>
    </nav>

    <!-- Active section -->
    <div class="profile-body">
      <LanguageSelector    v-if="tab === 'lang'"     />
      <BaseCurrencyManager v-else-if="tab === 'curr'" />
      <ChangePassword      v-else-if="tab === 'password'" />
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
