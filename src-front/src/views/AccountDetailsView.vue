<script setup>
import { onBeforeMount, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';
import { AccountService } from '../services/accounts';

const route = useRoute();
const accountStore = useAccountStore();
const userStore = useUserStore();
const accountService = new AccountService(userStore, accountStore);

let accountDetails = reactive({});

onBeforeMount(async () => {
  try {
    const details = await accountService.getAccountDetails(route.params.id);
    accountDetails = Object.assign(accountDetails, details);
  } catch(e) {
    console.log(e);
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
        <div class="col">Balance: {{ accountDetails.balance }}</div>
      </div>
      <div class="row">
        <div class="col">Open Date: {{ accountDetails.opening_date }}</div>
      </div>
    </div>
  </main>
</template>