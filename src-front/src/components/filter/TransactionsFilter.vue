<script setup>
import { onMounted, reactive, watch } from 'vue';

import TransactionType from './TransactionType.vue';
import AccountsListContainer from '@/components/filter/AccountsListContainer.vue';
import DateFilter from '@/components/filter/DateFilter.vue';

const props = defineProps(['transactions', 'resetstatus', 'isAccountDetails', 'accountId']);
const emit = defineEmits(['filterApplied']);

let filtersApplied = {};
const checkedAccounts = reactive([]);
const transactionTypes = reactive({
  'expense': false,
  'income': false,
  'transfer': false,
});

function resetFilters() {
  filtersApplied = {}; //remove all filters
  //disable all transaction types
  for (const prop in transactionTypes) {
    transactionTypes[prop] = false;
  }
  checkedAccounts.splice(0); //remove all selected accounts

  updateFilteredTransactions(true);
}

watch(() => props['resetstatus'], (newReset) => {
  if (newReset) {
    resetFilters();
  }
});

watch(() => props['accountId'], (newAccountId) => {
  if (newAccountId) {
    checkedAccounts.splice(0);
    checkedAccounts.push(newAccountId);
  }
});

function transactionTypeChanged({ newTransactionTypes }) {
  const { expense, income, transfer } = newTransactionTypes;
  transactionTypes.expense = expense;
  transactionTypes.income = income;
  transactionTypes.transfer = transfer;
  if (expense || income || transfer) {
    filtersApplied.transactionTypes = newTransactionTypes;
  } else {
    filtersApplied.transactionTypes = null;
  }
}

function selectedAccountsUpdated({ selectedAccounts }) {
  if (selectedAccounts.length > 0) {
    filtersApplied.accounts = selectedAccounts;
    checkedAccounts.splice(0);
    checkedAccounts.push(...selectedAccounts);
  } else {
    filtersApplied.accounts = [];
  }
}

function applyFilter(event) {
  event.preventDefault();
  updateFilteredTransactions();
}

function updateFilteredTransactions(newResetStatus = false) {
  filtersApplied.accounts = checkedAccounts;
  filtersApplied.fromDate = filtersApplied.startDate;
  filtersApplied.toDate = filtersApplied.endDate;

  emit('filterApplied', {
    'filterParams': filtersApplied,
    'resetStatus': newResetStatus,
  });
}

function updateFilterDates({ startDate, endDate }) {
  filtersApplied.startDate = startDate;
  filtersApplied.endDate = endDate;
}

</script>

<template>
  <div class="container filter-container">
    <TransactionType @transaction-type-changed="transactionTypeChanged" :types="transactionTypes" />

    <DateFilter @update-dates="updateFilterDates" />

    <AccountsListContainer v-show="props.isAccountDetails===false"
                           @selected-accounts-updated="selectedAccountsUpdated"
                           :selected-accounts="checkedAccounts" />

    <div class="row filter-bottom-menu-row">
      <div class="col bottom-menu-container">
        <a href="#" class="btn btn-primary me-2" @click="applyFilter">Apply</a>
        <a href="#" class="btn btn-secondary" @click="resetFilters">Reset</a>
      </div>
    </div>
  </div>

</template>

<style lang="scss" scoped>
@import '@/assets/common.scss';

.filter-container {
  margin-bottom: 1vh;
  background-color: $section-background-color;
  padding: 0.5rem;
}

.filter-bottom-menu-row {
  margin-top: 1vh;
}

.bottom-menu-container {
  display: flex;
  justify-content: start;
}
</style>