<script setup>
import { ref } from 'vue';

import LanguageSelector from './LanguageSelector.vue';
import BaseCurrencyManager from './BaseCurrencyManager.vue';
import ModalWindow from '../utils/ModalWindow.vue';

defineProps({
  closeModal: Function,
  showProfileModal: Boolean,
});

const showLanguageModal = ref(false);
const showCurrencyModal = ref(false);

const closeLanguageModal = () => {
  showLanguageModal.value = false;
};

const closeCurrencyModal = () => {
  showCurrencyModal.value = false;
};

const openLanguageModal = () => {
  showLanguageModal.value = true;
};

const openCurrencyModal = () => {
  showCurrencyModal.value = true;
};
</script>

<template>
  <ModalWindow :close-modal="closeModal">
    <template #header>
      <div class="row">
        <h2>{{ $t('message.profile') }}</h2>
      </div>
    </template>

    <template #main>
      <div class="row">
        <div class="col-12 lang-section">
          <button @click="openLanguageModal" class="btn btn-primary w-100 mb-2">{{ $t('buttons.language') }}</button>
        </div>

        <div class="col-12 currency-section">
          <button @click="openCurrencyModal" class="btn btn-primary w-100">{{ $t('buttons.baseCurrency') }}</button>
        </div>
      </div>
    </template>
  </ModalWindow>
  <teleport to="body" v-if="showLanguageModal">
    <LanguageSelector :close-language-modal="closeLanguageModal" :close-modal="closeLanguageModal" />
  </teleport>

  <teleport to="body" v-if="showCurrencyModal">
    <BaseCurrencyManager :close-currency-modal="closeCurrencyModal" />
  </teleport>


</template>

<style scoped>
.language-selector {
  z-index: 1100;
}
</style>