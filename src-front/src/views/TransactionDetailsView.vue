<script setup>
import { onBeforeMount, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { DateTime } from 'luxon';

import { Services } from '../services/servicesConfig';
import { HttpError } from '../errors/HttpError';

const router = useRouter();
const route = useRoute();

let transaction = reactive({});

onBeforeMount(async () => {
  try {
    const details = await Services.transactionsService.getTransactionDetails(route.params.id);
    transaction = Object.assign(transaction, details);
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
        <div class="col"><strong>{{ transaction.label }}</strong></div>
      </div>
      <div class="row">
        <div class="col"><strong>Amount:</strong> {{ transaction.amount }}{{ transaction.currency ?
          transaction.currency.code : '' }}</div>
      </div>
      <div class="row">
        <div class="col"><strong>Date and time:</strong> {{ DateTime.fromISO(transaction.datetime).toFormat('dd/MM/yyyy HH:mm') }}</div>
      </div>
      <div class="row">
        <div class="col"><strong>Notes:</strong> {{ transaction.notes }}</div>
      </div>
    </div>
  </main>
</template>