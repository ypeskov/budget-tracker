<script setup>
import LanguageSelector from './LanguageSelector.vue';
import { ref } from 'vue';

defineProps({
  closeModal: Function,
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
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h2>{{ $t('message.profile') }}</h2>
      <div class="container">

        <div class="row">
          <div class="col-12 lang-section">
            <button @click="openLanguageModal" class="btn btn-primary w-100">{{ $t('buttons.language') }}</button>
          </div>
          <teleport to="body">
            <LanguageSelector v-if="showLanguageModal" :close-language-modal="closeLanguageModal" />
          </teleport>
        </div>

      </div>
      <div class="row">
        <button class="btn btn-secondary" @click="closeModal">{{ $t('buttons.cancel') }}</button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;

}

.row {
  margin-top: 20px;
  margin-left: 0;
  width: 100%;
}
</style>