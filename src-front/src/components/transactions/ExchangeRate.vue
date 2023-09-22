<script setup>
import { computed } from 'vue';

const props = defineProps(['amountSrc', 'targetAmount', 'currencySrc', 'currencyTarget']);

const echangeRate = computed(() => {
  return props.targetAmount / props.amountSrc;
});

const reversedExhangedRate = computed(() => {
  return props.amountSrc / props.targetAmount;
});

</script>

<template>
  <div>{{ currencySrc }} / {{ currencyTarget }}: {{ echangeRate.toFixed(4) }}</div>
  <div class="mb-2">{{ currencyTarget }} / {{ currencySrc }}: ({{ reversedExhangedRate.toFixed(4) }})</div>
</template>

<style scoped></style>
