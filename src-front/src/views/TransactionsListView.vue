<script setup>
import { onBeforeMount, reactive } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { DateTime } from 'luxon';

import { useUserStore } from '../stores/user';
import { UserService } from '../services/users';
import { TransactionsService } from '../services/transactions';
import { HttpError } from '../errors/HttpError';

let transactions = reactive([]);
const userStore = useUserStore();
const userService = new UserService(userStore);
const router = useRouter();
const transactionsService = new TransactionsService(userService);

onBeforeMount(async () => {
  try {
    transactions.length = 0;
    transactions.push(...await transactionsService.getUserTransactions());
  } catch (e) {
    if (e instanceof HttpError && e.statusCode === 401) {
      console.log(e.message);
      router.push({ name: 'login' });
      return;
    } else {
      console.log(e);
    }
    router.push({ name: 'home' });
  }
});
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <h3>Your transactions</h3>
        </div>
      </div>
      <div v-if="transactions.length > 0">
        <div v-for="transaction in transactions" :key="transaction.id" class="list-item row">
          <div class="col-4 transaction-element">
            <RouterLink :to="{ name: 'transactionDetails', params: { id: transaction.id } }">
              {{ transaction.label }}
            </RouterLink>
          </div>
          <div class="col">
            {{ transaction.account.name }}
          </div>
          <div class="col">
            {{ transaction.amount }} {{ transaction.currency.code }}
          </div>
          <div class="col">
            {{ DateTime.fromISO(transaction.datetime).toLocaleString() }}
          </div>
        </div>
      </div>
      <div v-else>
        No transactions found
      </div>
    </div>
  </main>
</template>

<style scoped>
.transaction-element {
  overflow-wrap: break-word;
}
</style>