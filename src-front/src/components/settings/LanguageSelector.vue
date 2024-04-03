<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { Services } from '../../services/servicesConfig';
import { processError } from '../../errors/errorHandlers';
import ModalWindow from '../utils/ModalWindow.vue';

const props = defineProps({
  closeLanguageModal: Function,
});

const router = useRouter();
const languages = reactive([]);
const { locale } = useI18n();
const selectedLanguage = ref('');

onBeforeMount(async () => {
  languages.length = 0;
  try {
    languages.push(...await Services.settingsService.getLanguages());
    selectedLanguage.value = languages.find((language) => language.code === locale.value)?.id;
  } catch (error) {
    await processError(error, router);
  }
});

const handleLanguageChange = () => {
  // console.log(languages.find((language) => language.id === selectedLanguage.value).name);
};

const applyAndClose = async () => {
  locale.value = languages.find((language) => language.id === selectedLanguage.value)?.code;
  Services.userService.userStore.settings.language = locale.value;
  try {
    await Services.settingsService.saveUserSettings();
  } catch (error) {
    await processError(error, router);
  }

  props.closeLanguageModal();
};

</script>

<template>
  <ModalWindow :close-modal="props.closeLanguageModal" modal-id="language-selector">
    <template #header>
      <div class="row">
        <h2>{{ $t('message.select_language') }}</h2>
      </div>
    </template>
    <template #main>
      <h2>{{ $t('message.select_language') }}</h2>
      <select class="form-select mb-3" v-model="selectedLanguage" @change="handleLanguageChange">
        <option v-for="language in languages" :value="language.id" :key="language.id">{{ language.name }}</option>
      </select>
      <button class="btn btn-primary" @click="applyAndClose">{{ $t('buttons.apply') }}</button>
    </template>
  </ModalWindow>
</template>


<style scoped>
.btn-primary, .btn-secondary {
  margin-top: 10px;
}

.language-selector {
  z-index: 1100;
}
</style>