<script setup>
import { onBeforeMount, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';
import { AccountService } from '../services/accounts';
import { HttpError } from '../errors/HttpError';

const route = useRoute();
const router = useRouter();
const accountStore = useAccountStore();
const userStore = useUserStore();
const accountService = new AccountService(userStore, accountStore);

let accountDetails = reactive({});

onBeforeMount(async () => {
  try {
    const details = await accountService.getAccountDetails(route.params.id);
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
      <div class="row">
        <div class="col">
          Account: <strong>{{ accountDetails.name }}</strong>
        </div>
      </div>
      <div class="row">
        <div class="col">Balance: {{ accountDetails.balance }} {{ accountDetails?.currency?.code }}</div>
      </div>
      <div class="row">
        <div class="col">Open Date: {{ accountDetails.opening_date }}</div>
      </div>
    </div>
  </main>
</template>