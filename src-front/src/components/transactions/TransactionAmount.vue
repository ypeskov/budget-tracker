<script setup>
import { computed } from 'vue';

const props = defineProps(['transaction', 'currentAccount', 'label', 'type']);
const emit = defineEmits(['amountChanged']);

const amount = computed(() => {
  if (type === 'src') {
    return transaction.amount;
  } else if (type === 'target') {
    return transaction.target_amount;
  }
})

function changeAmount($value) {
  emit('amountChanged', {
    amountType: props.type,
    amount: parseFloat($value.target.value)
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
        <input type="number" @keyup="changeAmount" class="form-control" id="amount" step="0.01" />
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
