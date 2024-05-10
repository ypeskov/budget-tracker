<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import { Services } from '../services/servicesConfig';
import { processError } from '../errors/errorHandlers';
import newAccount from '../components/account/newAccount.vue';

const router = useRouter();

let accounts = reactive([]);
const showNewAccForm = ref(false);
const showHiddenAccounts = ref(false);

onBeforeMount(async () => {
  try {
    await reReadAllAccounts();
  } catch (e) {
    await processError(e, router);
  }
});

async function reReadAllAccounts(shouldUpdate = false) {
  accounts.length = 0;
  try {
    const tmpAccounts = await Services.accountsService.getUserAccounts(showHiddenAccounts.value, shouldUpdate);
    if (tmpAccounts) {
      accounts.push(...tmpAccounts);
    }
  } catch (e) {
    await processError(e, router);
  }
}

async function updateAccountsList(event) {
  if (event) {
    event.preventDefault();
  }
  await reReadAllAccounts(true);
}

async function accountCreated() {
  await updateAccountsList();
  closeNewAccForm();
}

function closeNewAccForm() {
  showNewAccForm.value = false;
}

function toggleHiddenAccounts(event) {
  showHiddenAccounts.value = event.target.checked;
  reReadAllAccounts(true);
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <label class="btn btn-secondary">
            <input type="checkbox" @change="toggleHiddenAccounts">
            {{ $t('message.showHiddenAccounts') }}
          </label>
        </div>
        <div class="col sub-menu">
          <a href="javascript:void(0);"
             class="btn btn-secondary"
             @click.prevent="showNewAccForm=!showNewAccForm">
            <img src="/images/icons/new-icon.svg"
                 :title="$t('message.newAccount')"
                 :alt="$t('message.newAccount')" />
          </a>
          <a href="javascript:void(0);"
             class="btn btn-secondary"
             @click="updateAccountsList">
            <img src="/images/icons/refresh-icon.svg"
                 :title="$t('message.refresh')"
                 :alt="$t('message.refresh')" />
          </a>
        </div>
      </div>

      <div v-if="showNewAccForm" class="row">
        <div class="col">
          <newAccount :account-created="accountCreated" :close-new-acc-form="closeNewAccForm" />
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
            <div class="col-5 account-name">
              {{ acc.name }}
            </div>
            <div class="col account-balance">
              <b>{{ $n(acc.balance, 'decimal') }}</b> {{ acc.currency.code }}
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </main>
</template>

<style scoped>
@import '../assets/main.scss';

.account-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.account-balance {
  text-align: right;
}

.list-item > a {
  text-decoration: none;
  color: black;
}
</style>