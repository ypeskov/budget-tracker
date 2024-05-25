<script setup>
import { onBeforeMount, reactive } from 'vue';

import { Services } from '@/services/servicesConfig';
import ModalWindow from '@/components/utils/ModalWindow.vue';

const props = defineProps({
  closeCurrencyModal: Function,
});

let selectedCurrency = reactive({});
const currencies = reactive([]);

onBeforeMount(async () => {
  const baseCurrency = await Services.settingsService.getBaseCurrency();
  Object.assign(selectedCurrency, baseCurrency);
  const allCurrencies = await Services.currenciesService.getAllCurrencies();
  currencies.length = 0;
  currencies.push(...allCurrencies);
});

const handleCurrencyChange = (event) => {
  const newCurrencyCode = event.target.value;
  const currency = currencies.find(c => c.code === newCurrencyCode);
  if (currency) {
    Object.assign(selectedCurrency, currency);
  }
}

const applyAndClose = async () => {
  await Services.settingsService.setBaseCurrency(selectedCurrency);
  props.closeCurrencyModal();
}
</script>

<template>
  <ModalWindow :close-modal="props.closeCurrencyModal" modal-id="language-selector">
    <template #header>
      <div class="row">
        <h2>{{ $t('message.selectBaseCurrency') }}</h2>
      </div>
    </template>
    <template #main>
      <div>{{ $t('message.currentCurency') }}: {{ selectedCurrency.code }}</div>
      <select class="form-select mb-3" v-model="selectedCurrency.code" @change="handleCurrencyChange">
        <option v-for="currency in currencies"
                :value="currency.code"
                :key="currency.id">{{ currency.code }} ({{ currency.name }})</option>
      </select>
      <button class="btn btn-primary" @click="applyAndClose">{{ $t('buttons.apply') }}</button>
    </template>
  </ModalWindow>
</template>

<style scoped>

</style>