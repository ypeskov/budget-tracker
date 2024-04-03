<script setup>
import { ref } from 'vue';

import LanguageSelector from './LanguageSelector.vue';
import ModalWindow from '../utils/ModalWindow.vue';

defineProps({
  closeModal: Function,
  showProfileModal: Boolean,
  'close-modal': Function,
});

const showLanguageModal = ref(false);

const closeLanguageModal = () => {
  showLanguageModal.value = false;
};

const openLanguageModal = () => {
  showLanguageModal.value = true;
};
</script>

<template>
  <ModalWindow v-if="showProfileModal" :close-modal="closeModal">
    <template #header>
      <div class="row">
        <h2>{{ $t('message.profile') }}</h2>
      </div>
    </template>

    <template #main>
      <div class="row">
        <div class="col-12 lang-section">
          <button @click="openLanguageModal" class="btn btn-primary w-100">{{ $t('buttons.language') }}</button>
        </div>
      </div>
    </template>
  </ModalWindow>
  <teleport to="body" v-if="showLanguageModal">
    <LanguageSelector :close-language-modal="closeLanguageModal" />
  </teleport>

</template>

<style scoped>
.language-selector {
  z-index: 1100;
}
</style>