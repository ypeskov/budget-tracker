<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import { Services } from '../services/servicesConfig';
import { processError } from '../errors/errorHandlers';
import newAccount from '../components/account/newAccount.vue';
import { DateTime } from 'luxon';

const router = useRouter();

let accounts = reactive([]);
const showNewAccForm = ref(false);
const showHiddenAccounts = ref(false);
const totalBalance = ref(0);
const baseCurrencyCode = ref('');
const today = DateTime.now().toISODate();

onBeforeMount(async () => {
  try {
    await reReadAllAccounts(true);
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

    const accountIds = accounts.map((acc) => acc.id);
    const accountBalancesInBaseCurrency = await Services.reportsService
      .getReport('balance/non-hidden', {
        accountIds: accountIds,
        'balanceDate': today,
      });

    if (accountBalancesInBaseCurrency.length > 0) {
      totalBalance.value = accountBalancesInBaseCurrency.reduce((acc, item) => acc + item.baseCurrencyBalance, 0);
      baseCurrencyCode.value = accountBalancesInBaseCurrency[0].baseCurrencyCode;
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

function balanceClass(balance) {
  return balance < 0 ? 'text-danger' : 'text-success';
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
          <div>
            <b>{{ $t('message.yourAccounts') }}</b>
            ( {{ $t('message.totalBalance') }}: {{ $n(totalBalance, 'decimal') }} {{ baseCurrencyCode }})
          </div>
        </div>
      </div>
      <div v-for="acc in accounts" :key="acc.id" class="list-item">
        <RouterLink class="account-link" :to="{name: 'accountDetails', params: {id: acc.id}}">
          <div class="row account-item">
            <div class="col-4 account-name">
              {{ acc.name }}
            </div>
            <div class="col account-balance" :class="balanceClass(acc.balance)">
              <b>{{ $n(acc.balance, 'decimal') }}</b> {{ acc.currency.code }}
            </div>
            <div class="col-2 account-marks">
              <span v-if="acc.showInReports"
                    :title="$t('message.showInReports')"
                    class="badge bg-success">&#10003;</span>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </main>
</template>

<style scoped lang="scss">
@use '@/assets/main.scss' as *;

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

.account-marks {
  text-align: right;
}
</style>