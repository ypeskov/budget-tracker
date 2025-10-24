<script setup>
import { ref, defineExpose } from 'vue';

const props = defineProps(['amount', 'currentAccount', 'label', 'type',]);
const emit = defineEmits(['amountChanged']);

const amountInput = ref(null);
defineExpose({ amountInput });

const inputValue = ref(String(props.amount ?? ''));

function changeAmount(event) {
  let raw = event.target.value.replace(',', '.');
  inputValue.value = raw;

  const parsed = parseFloat(raw);
  if (!isNaN(parsed)) {
    emit('amountChanged', {
      amountType: props.type,
      amount: parsed,
    });
  }
}
</script>

<template>
  <div class="mb-3">
    <div class="row">
      <div class="col-10">
        <label for="amount" class="form-label">
          {{ label }}
        </label>
        <input
          type="text"
          ref="amountInput"
          @input="changeAmount"
          :value="inputValue"
          class="form-control"
          pattern="[0-9.]*"
          inputmode="decimal"
        />
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
