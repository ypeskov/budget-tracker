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
        <div class="col"><strong>{{ transaction.short_description }}</strong></div>
      </div>
      <div class="row">
        <div class="col"><strong>Amount:</strong> {{ transaction.amount }}{{ transaction.currency ?
          transaction.currency.code : '' }}</div>
      </div>
      <div class="row">
        <div class="col"><strong>Date and time:</strong> {{ transaction.datetime }}</div>
      </div>
      <div class="row">
        <div class="col"><strong>Notes:</strong> {{ transaction.long_description }}</div>
      </div>
    </div>
  </main>
</template>