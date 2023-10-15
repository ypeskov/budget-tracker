<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';
import { AccountService } from '../services/accounts';
import { HttpError } from '../errors/HttpError';
import newAccount from '../components/account/newAccount.vue';

let accounts = reactive([]);
const userStore = useUserStore();
const accountStore = useAccountStore();
const accountService = new AccountService(userStore, accountStore);
const router = useRouter();

const showNewAccForm = ref(false);

onBeforeMount(async () => {
  try {
    accounts.splice(0);
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

async function updateAccuntsList(event) {
  event.preventDefault();
  accountService.setShouldUpdateAccountsList(true);
  try {
    accounts.splice(0);
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
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col sub-menu">
          <a href="" class="btn btn-secondary" @click="updateAccuntsList">Reload</a>
          <a href="" class="btn btn-secondary" @click.prevent="showNewAccForm=!showNewAccForm">New Account</a>
        </div>
      </div>

      <div v-if="showNewAccForm" class="row">
        <div class="col"><newAccount /></div>
      </div>

      <div class="row">
        <div class="col">
          <h3>Your accounts</h3>
        </div>
      </div>
        <div v-for="acc in accounts" :key="acc.id" class="list-item">
          <RouterLink class="account-link" :to="{name: 'accountDetails', params: {id: acc.id}}">
            <div class="row account-item">
              <div class="col-4">
              {{ acc.name }}
              </div>
              <div class="col-2">
                {{ acc.account_type.type_name }}
              </div>
              <div class="col account-balance">
                {{ acc.balance }} {{ acc.currency.code }}
              </div>
            </div>
          </RouterLink>
        </div>
    </div>
  </main>
</template>

<style scoped>
@import '../assets/main.scss';
.account-balance {
  text-align: right;
}
.list-item>a {
  text-decoration: none;
  color: black;
}
</style>