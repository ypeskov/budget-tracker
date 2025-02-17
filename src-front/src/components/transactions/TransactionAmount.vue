<script setup>
import { ref, defineExpose } from 'vue';

const props = defineProps(['amount', 'currentAccount', 'label', 'type',]);
const emit = defineEmits(['amountChanged']);

const amountInput = ref(null);
defineExpose({ amountInput });

function changeAmount($value) {
  let value = $value.target.value;
  value = value.replace(',', '.');
  const updatedAmount = value;
  emit('amountChanged', {
    amountType: props.type,
    amount: parseFloat(updatedAmount) || 0,
  });
}
</script>

<template>
  <div class="mb-3">
    <div class="row">
      <div class="col-10">
        <label for="amount" class="form-label">
          {{ label }}
        </label>
        <input type="text"
               ref="amountInput"
               @input="changeAmount"
               :value="amount"
               class="form-control"
               pattern="[0-9.]*"
               inputmode="decimal" />
      </div>
      <div class="col-2 currency">{{ currentAccount?.currency?.code }}</div>
    </div>
  </div>
</template>

<style scoped>
.currency {
  align-self: flex-end;
}
</style>
