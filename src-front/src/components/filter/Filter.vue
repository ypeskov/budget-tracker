<script setup>
import TransactionType from './TransactionType.vue';

const props = defineProps(['transactions']);
const emit = defineEmits(['filterApplied']);

const possibleFilters = ['transactionTypes', 'categories', 'currencies', 'accounts',];
const filtersApplied = {};

function transactionTypeChanged({transactionTypes}) {
  const {expense, income, transfer} = transactionTypes;
  if (expense || income || transfer) {
    filtersApplied.transactionTypes = transactionTypes;
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

  emit('filterApplied', filteredTransactions);
}

function filterByType(transTypes) {
  return props['transactions'].filter(trans => {
    if (transTypes.expense === true) {
      if (trans.is_income === false) {
        return true;
      }
    }
    if (transTypes.income === true) {
      if (trans.is_income === true) {
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
    <TransactionType @transaction-type-changed="transactionTypeChanged" />
  </div>
</template>

<style scoped>
.filter-container {
  margin-bottom: 1vh;
}
</style>