<script setup>
import { onBeforeMount, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { UserService } from '../services/users';
import { useUserStore } from '../stores/user';
import { TransactionsService } from '../services/transactions';

const route = useRoute();
const userStore = useUserStore();
const transactionsService = new TransactionsService(new UserService(userStore));

let transaction = reactive({});

onBeforeMount(async () => {
  try {
    const details = await transactionsService.getTransactionDetails(route.params.id);
    transaction = Object.assign(transaction, details);
  } catch (e) {
    console.log(e);
  }
});
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">{{ transaction.short_description }}</div>
      </div>
      <div class="row">
        <div class="col">Amount: {{ transaction.amount }}</div>
      </div>
      <div class="row">
        <div class="col">Date and time: {{ transaction.datetime }}</div>
      </div>
      <div class="row">
        <div class="col">Notes: {{ transaction.long_description }}</div>
      </div>
    </div>
  </main>
</template>