<script setup>
import { reactive } from 'vue';

const emit = defineEmits(['transactionTypeChanged']);

const types = reactive({
  'expense': false,
  'income': false,
  'transfer': false,
});

function transactionTypeChanged(event) {
  const status = event.target.checked;
  const transType = event.target.value;
  types[transType] = status;
  emit('transactionTypeChanged', {
    'transactionTypes': {...types},
  });
}
</script>

<template>
  <div class="checkboxes-container">
    <span class="one-checkbox-container">
      <input class="form-check-input" type="checkbox" value="expense" id="expense-check"
             @click="transactionTypeChanged" :checked="types.expense">
      <label class="form-check-label" for="expense-check">Expense</label>
    </span>
    <span class="one-checkbox-container">
      <input class="form-check-input" type="checkbox" value="income" id="income-check" 
             @click="transactionTypeChanged" :checked="types.income">
      <label class="form-check-label" for="income-check">Income</label>
    </span>
    <span class="one-checkbox-container">
      <input class="form-check-input" type="checkbox" value="transfer" id="transfer-check"
             @click="transactionTypeChanged" :checked="types.transfer">
      <label class="form-check-label" for="transfer-check">Transfer</label>
    </span>
  </div>
</template>

<style scoped>
.checkboxes-container {
  display: flex;
  justify-content: start;
}
.one-checkbox-container {
  margin-right: 5vw;
}
</style>