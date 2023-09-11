<script setup>
import { onBeforeMount, reactive } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import { useUserStore } from '../stores/user';
import { TransactionsService } from '../services/transactions';

let transactions = reactive([]);
const userStore = useUserStore();
const router = useRouter();
const transactionsService = new TransactionsService(userStore);

onBeforeMount(async () => {
  try {
    transactions.length = 0;
    transactions.push(...await transactionsService.getUserTransactions());
  } catch (e) {
    console.log(e.message);
    router.push({ name: 'login' })
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
        <div v-for="transaction in transactions" :key="transaction.id" class="list-item">
          <RouterLink :to="{name: 'transactionDetails', params: {id: transaction.id}}">
            <div class="row">
              <div class="col">
              {{ transaction.short_description }}
              </div>
              <div class="col">
                {{ transaction.amount }}
              </div>
            </div>
          </RouterLink> 
        </div>
    </div>
  </main>
</template>