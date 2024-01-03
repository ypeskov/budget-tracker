<script setup>
import { onBeforeMount, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { DateTime } from 'luxon';

import { Services } from '../services/servicesConfig';
import { HttpError } from '../errors/HttpError';

import TransactionsListView from './TransactionsListView.vue';

const route = useRoute();
const router = useRouter();

let accountDetails = reactive({});

onBeforeMount(async () => {
  try {
    const details = await Services.accountsService.getAccountDetails(route.params.id);
    accountDetails = Object.assign(accountDetails, details);
  } catch(e) {
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
      <div class="account-row">
        <div class="account-name">
          Account: <strong>{{ accountDetails.name }}</strong>
        </div>
      </div>
    </div>

    <TransactionsListView :account-id="accountDetails.id" :is-account-details="true" />
  </main>
</template>


<style scoped>
.container {
  margin: 0 auto;
  /* padding: 10px 0;  */
}

.account-row {
  background-color: #e2e0e0;
  padding: 5px 10px;
  border-radius: 5px;
  margin: 0.5rem 0 0.5rem 0.5rem;
}

.account-name {
  font-size: 1em;
  color: #333;
}
</style>

