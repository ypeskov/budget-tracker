<script setup>
import { computed } from 'vue';

const props = defineProps(['transaction', 'currentAccount', 'label', 'type', 'linkedTransaction']);
const emit = defineEmits(['amountChanged']);

const amount = computed(() => {
  if (props.type === 'src') {
    return props.transaction.amount;
  } else  {
    return props.linkedTransaction.amount;
  }
});

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
