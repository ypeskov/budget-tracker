<script setup>
import {computed, onBeforeMount, reactive, ref} from 'vue';
import {RouterLink, useRouter} from 'vue-router';

import {Services} from '../services/servicesConfig';
import {HttpError} from '../errors/HttpError';
import newAccount from '../components/account/newAccount.vue';

let accounts = reactive([]);

const router = useRouter();

const showNewAccForm = ref(false);

onBeforeMount(async () => {
  try {
    accounts.splice(0);
    accounts.push(...await Services.accountsService.getAllUserAccounts());
  } catch (e) {
    if (e instanceof HttpError && e.statusCode === 401) {
      console.log(e.message);
      await router.push({name: 'login'});
      return;
    } else {
      console.log(e);
    }
    await router.push({name: 'home'});
  }
});

const totalBalance = computed(() => {
  return accounts.reduce((acc, item) => acc + item.balance, 0);
});

async function updateAccountsList(event) {
  if (event) {
    event.preventDefault();
  }

  Services.accountsService.setShouldUpdateAccountsList(true);
  try {
    accounts.splice(0);
    accounts.push(...await Services.accountsService.getAllUserAccounts());
  } catch (e) {
    if (e instanceof HttpError && e.statusCode === 401) {
      console.log(e.message);
      await router.push({name: 'login'});
      return;
    } else {
      console.log(e);
    }
    await router.push({name: 'home'});
  }
}

function formattedBalance(balance) {
  return balance.toLocaleString('ru-UA', {
    style: 'decimal',
    maximumFractionDigits: 2,
    minimumFractionDigits: 2
  });
}

async function accountCreated() {
  await updateAccountsList();
  closeNewAccForm();
}

function closeNewAccForm() {
  showNewAccForm.value = false;
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col sub-menu">
          <a href="" class="btn btn-secondary" @click="updateAccountsList">{{ $t('message.reload') }}</a>
          <a href="" class="btn btn-secondary" @click.prevent="showNewAccForm=!showNewAccForm">
            {{ $t('message.newAccount') }}
          </a>
        </div>
      </div>

      <div v-if="showNewAccForm" class="row">
        <div class="col">
          <newAccount :account-created="accountCreated" :close-new-acc-form="closeNewAccForm"/>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <div><b>{{ $t('message.yourAccounts') }}</b> (Total balance: <b>No idea</b>)</div>
        </div>
      </div>
      <div v-for="acc in accounts" :key="acc.id" class="list-item">
        <RouterLink class="account-link" :to="{name: 'accountDetails', params: {id: acc.id}}">
          <div class="row account-item">
            <div class="col-4">
              {{ acc.name }}
            </div>
            <div class="col account-balance">
              <b>{{ formattedBalance(acc.balance) }}</b> {{ acc.currency.code }}
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

.list-item > a {
  text-decoration: none;
  color: black;
}
</style>