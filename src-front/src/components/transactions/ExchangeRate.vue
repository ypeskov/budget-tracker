<script setup>
import { computed } from 'vue';

const props = defineProps(['amount', 'targetAmount',]);

const echangeRate = computed(() => {
  return props.targetAmount / props.amount;
})

</script>

<template>
  <div class="mb-3">Exchange Rate: {{ echangeRate }}</div>
</template>

<style scoped></style>
