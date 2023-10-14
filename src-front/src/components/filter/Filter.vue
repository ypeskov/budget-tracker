<script setup>
import { watch, reactive } from 'vue';
import TransactionType from './TransactionType.vue';

const props = defineProps(['transactions', 'resetstatus']);
const emit = defineEmits(['filterApplied']);

const possibleFilters = ['transactionTypes', 'categories', 'currencies', 'accounts',];
let filtersApplied = {};

const transactionTypes = reactive({
  'expense': false,
  'income': false,
  'transfer': false,
});

watch(() => props['resetstatus'], (newReset) => {
  if (newReset) {
    filtersApplied = {};
    for(const prop in transactionTypes) {
      transactionTypes[prop] = false;
    }
    updateFilteredTransactions();
  }
});

function transactionTypeChanged({newTransactionTypes}) {
  const {expense, income, transfer} = newTransactionTypes;
  transactionTypes.expense = expense;
  transactionTypes.income = income;
  transactionTypes.transfer = transfer;
  if (expense || income || transfer) {
    filtersApplied.transactionTypes = newTransactionTypes;
  } else {
    filtersApplied.transactionTypes = null;
  }
  
  updateFilteredTransactions();
}



function updateFilteredTransactions() {
  let filteredTransactions = [...props['transactions']];
  if (filtersApplied.transactionTypes) {
    filteredTransactions = filterByType(filtersApplied.transactionTypes);
  }

  emit('filterApplied', {
    'filteredTransactions': filteredTransactions,
    'resetStatus': false,
  });
}

function filterByType(transTypes) {
  return props['transactions'].filter(trans => {
    if (transTypes.expense === true) {
      if (trans.is_income === false && trans.is_transfer === false) {
        return true;
      }
    }
    if (transTypes.income === true) {
      if (trans.is_income === true && trans.is_transfer === false) {
        return true;
      }
    }
    if (transTypes.transfer === true) {
      if (trans.is_transfer === true) {
        return true;
      }
    }
  });
}
</script>

<template>
  <div class="filter-container">
    <TransactionType @transaction-type-changed="transactionTypeChanged" :types="transactionTypes" />
  </div>
</template>

<style scoped>
.filter-container {
  margin-bottom: 1vh;
}
</style>