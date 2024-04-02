<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { Services } from '../../services/servicesConfig';
import { processError} from '../../errors/errorHandlers';

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
.btn-primary, .btn-secondary {
  margin-top: 10px;
}
</style>