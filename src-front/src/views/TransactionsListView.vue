<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { DateTime } from 'luxon';

import { useUserStore } from '../stores/user';
import { UserService } from '../services/users';
import { TransactionsService } from '../services/transactions';
import { HttpError } from '../errors/HttpError';
import Filter from '../components/filter/Filter.vue';

let transactions = reactive([]);
let filteredTransactions = reactive([]);
const userStore = useUserStore();
const userService = new UserService(userStore);
const router = useRouter();
const transactionsService = new TransactionsService(userService);
const showFilter = ref(false);
const reset = ref(false);

onBeforeMount(async () => {
  try {
    transactions.splice(0);
    const allTransactions = await transactionsService.getUserTransactions();
    transactions.push(...allTransactions);
    filteredTransactions.push(...allTransactions);
  } catch (e) {
    if (e instanceof HttpError && e.statusCode === 401) {
      router.push({ name: 'login' });
      return;
    } else {
      console.log(e);
    }
    router.push({ name: 'home' });
  }
});

async function reloadTransactions(event) {
  event.preventDefault();
  const allTransactions = await transactionsService.getUserTransactions();
  transactions.splice(0);
  transactions.push(...allTransactions);
  filteredTransactions.splice(0);
  filteredTransactions.push(...allTransactions);
  reset.value = true;
}

function toggleFilter(event) {
  event.preventDefault();
  showFilter.value = !showFilter.value;
}

function filterApplied(payload) {
  filteredTransactions.splice(0);
  filteredTransactions.push(...payload.filteredTransactions);
  reset.value = payload.resetStatus;
  showFilter.value = false;
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col sub-menu">
          <a href="" class="btn btn-secondary" @click="reloadTransactions">Reload</a>
          <a href="" class="btn btn-secondary" @click="toggleFilter">Filter</a>
        </div>
      </div>
      <div class="row">
        <div class="col" v-show="showFilter">
          <Filter @filter-applied="filterApplied" :transactions="transactions" :resetstatus="reset" />
        </div>
      </div>

      <div class="row">
        <div class="col">
          <h3>Your transactions</h3>
        </div>
      </div>
      <div v-if="transactions.length > 0">
        <div v-for="transaction, idx in filteredTransactions" :key="transaction.id" class="list-item">
          <RouterLink class="row" :to="{ name: 'transactionDetails', params: { id: transaction.id } }">
            <div class="col-7">
              <div class="transaction-element"><b>{{ transaction.label }}</b></div>
              <div class="transaction-element">{{ transaction.notes }}</div>
            </div>
            <div class="col-5 amount-container">
              <div><b>{{ parseFloat(transaction.amount).toFixed(2) }} {{ transaction.currency.code }}</b></div>
              <div>{{ DateTime.fromISO(transaction.date_time).toLocaleString() }}</div>
            </div>
          </RouterLink>
        </div>
      </div>
      <div v-else>
        No transactions found
      </div>
    </div>
  </main>
</template>

<style scoped>
@import '../assets/main.scss';

.transaction-element {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.amount-container {
  text-align: right;
}
</style>