<script setup>
import { onBeforeMount, reactive } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';
import {AccountService} from '../services/accounts';
import { HttpError } from '../errors/HttpError';

let accounts = reactive([]);
const userStore = useUserStore();
const accountStore = useAccountStore();
const accountService = new AccountService(userStore, accountStore);
const router = useRouter();

onBeforeMount(async () => {
  try {
    accounts.length = 0;
    accounts.push(...await accountService.getAllUserAccounts()); 
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
          <h3>Your accounts</h3>
        </div>
      </div>
        <div v-for="acc in accounts" :key="acc.id" class="list-item">
          <RouterLink :to="{name: 'accountDetails', params: {id: acc.id}}">
            <div class="row">
              <div class="col">
              {{ acc.name }}
              </div>
              <div class="col">
                {{ acc.account_type.type_name }}
              </div>
              <div class="col">
                {{ acc.balance }} {{ acc.currency.code }}
              </div>
            </div>
          </RouterLink>
          
        </div>
    </div>
  </main>
</template>