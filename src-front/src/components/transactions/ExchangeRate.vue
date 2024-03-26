<script setup>
import { computed } from 'vue';

const props = defineProps(['amountSrc', 'targetAmount', 'currencySrc', 'currencyTarget']);

const exchangeRate = computed(() => {
  return props.targetAmount / props.amountSrc;
});

const reversedExchangedRate = computed(() => {
  return props.amountSrc / props.targetAmount;
});

</script>

<template>
  <div>{{ currencySrc }} / {{ currencyTarget }}: {{ exchangeRate.toFixed(4) }}</div>
  <div class="mb-2">{{ currencyTarget }} / {{ currencySrc }}: ({{ reversedExchangedRate.toFixed(4) }})</div>
</template>

<style scoped></style>
