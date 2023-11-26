<script setup>
import { onBeforeMount, reactive, ref, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import { Services } from '../services/servicesConfig';
import { HttpError } from '../errors/HttpError';
import { useUserStore } from '../stores/user';
import Filter from '../components/filter/Filter.vue';
import List from '../components/transactions/List.vue';

const userStore = useUserStore();
let transactions = reactive([]);
let filteredTransactions = reactive([]);

const router = useRouter();

const showFilter = ref(false);
const reset = ref(true);

onBeforeMount(async () => {
  try {
    transactions.splice(0);
    const allTransactions = await Services.transactionsService.getUserTransactions();
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
  const allTransactions = await Services.transactionsService.getUserTransactions();
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
          <span v-if="userStore.isLoggedIn">
            <RouterLink class="btn btn-secondary" :to="{ name: 'transactionNew' }">New</RouterLink>
          </span>
          <span>
            <a href="" class="btn btn-secondary" @click="reloadTransactions">Reload</a>
          </span>
          <span>{{ reset }}
            <a href="" 
              class="btn" 
              :class="{ 'active-filter btn-success': !reset, 'btn-secondary': reset }"
              @click="toggleFilter">Filter</a>
          </span>
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
      <div class="row">
        <List :transactions="filteredTransactions" />
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

.active-filter {
  font-weight: bold;
  color: #ffffff;
}
</style>