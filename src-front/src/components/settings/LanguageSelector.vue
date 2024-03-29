<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { Services } from '../../services/servicesConfig';
import { HttpError } from '../../errors/HttpError';

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
    if (error instanceof HttpError) {
      console.error(error);
      router.push({ name: 'home' });
    }
  }
});

const handleLanguageChange = () => {
  // console.log(languages.find((language) => language.id === selectedLanguage.value).name);
};

const applyAndClose = () => {
  locale.value = languages.find((language) => language.id === selectedLanguage.value)?.code;
  Services.userService.userStore.settings.language = locale.value;
  Services.settingsService.saveUserSettings();
  props.closeLanguageModal();
};

</script>

<template>
  <div class="modal-overlay" @click="closeLanguageModal">
    <div class="modal-content" @click.stop>
      <h2>{{ $t('message.select_language') }}</h2>
      <select class="form-select mb-3" v-model="selectedLanguage" @change="handleLanguageChange">
        <option v-for="language in languages" :value="language.id" :key="language.id">{{ language.name }}</option>
      </select>
      <button class="btn btn-primary" @click="applyAndClose">{{ $t('buttons.apply') }}</button>
      <button class="btn btn-secondary" @click="closeLanguageModal">{{ $t('buttons.cancel') }}</button>

    </div>
  </div>
</template>


<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 500px;
}

.btn-primary, .btn-secondary {
  margin-top: 10px;
}
</style>