<script setup>
import { ref } from 'vue';
// import { useI18n } from 'vue-i18n';
// import { useRouter } from 'vue-router';
// import { Services } from '../services/servicesConfig';
// import { HttpError } from '../errors/HttpError';
import LanguageSelector from '../components/settings/LanguageSelector.vue';

// const router = useRouter();


const showLanguageModal = ref(false);

const openLanguageModal = () => {
  showLanguageModal.value = true;
};

const closeLanguageModal = () => {
  showLanguageModal.value = false;
};

</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h1>{{ $t('message.settings') }}</h1>
        </div>
      </div>

      <div class="row">
        <div class="col-12 profile-section">
          <a href="/settings/profile" class="btn btn-primary w-100">{{ $t('buttons.profile') }}</a>
        </div>
      </div>

      <div class="row">
        <div class="col-12 lang-section">
          <button @click="openLanguageModal" class="btn btn-primary w-100">{{ $t('buttons.language') }}</button>
        </div>

        <teleport to="body">
          <LanguageSelector v-if="showLanguageModal"
                            :show-language-modal="showLanguageModal"
                            :close-language-modal="closeLanguageModal" />
        </teleport>
      </div>
    </div>


  </main>
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