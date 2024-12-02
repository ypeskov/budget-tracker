<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

import { Services } from '@/services/servicesConfig';
import { processError } from '@/errors/errorHandlers';
import newAccount from '@/components/account/newAccount.vue';
import ArchivedAccountsList from '@/components/account/ArchivedAccountsList.vue';
import MainAccountsList from '@/components/account/MainAccountsList.vue';
import { DateTime } from 'luxon';

const router = useRouter();

let accounts = reactive([]);
let archivedAccounts = reactive([]);

const showNewAccForm = ref(false);
const showHiddenAccounts = ref(false);
const showArchivedAccounts = ref(false);
const showMainAccountsList = ref(true);
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

async function getArchivedAccounts(shouldUpdate = true) {
  try {
    const params = {
      shouldUpdate: shouldUpdate,
      archivedOnly: true,
    };
    archivedAccounts.length = 0;
    const tmpAccounts = await Services.accountsService.getUserAccounts(params);
    if (tmpAccounts) {
      archivedAccounts.push(...tmpAccounts);
    }
  } catch (e) {
    await processError(e, router);
  }
}

async function reReadAllAccounts(shouldUpdate = false) {
  accounts.length = 0;
  try {
    const params = {
      includeHidden: showHiddenAccounts.value,
      shouldUpdate: shouldUpdate,
      includeArchived: true,
      archivedOnly: false,
    };
    const tmpAccounts = await Services.accountsService.getUserAccounts(params);
    if (tmpAccounts) {
      accounts.push(...tmpAccounts);
    }

    await getArchivedAccounts();

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

function toggleArchivedAccounts(event) {
  showArchivedAccounts.value = event.target.checked;
  showMainAccountsList.value = !event.target.checked;
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <label v-if="!showArchivedAccounts" class="btn btn-secondary">
            <input type="checkbox" @change="toggleHiddenAccounts">
            {{ $t('message.showHiddenAccounts') }}
          </label>
        </div>
        <div class="col">
          <label class="btn btn-secondary">
            <input type="checkbox" @change="toggleArchivedAccounts">
            {{ $t('buttons.showArchivedAccounts') }}
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

      <div v-if="showArchivedAccounts">
        <archivedAccountsList :archived-accounts="archivedAccounts" :re-read-all-accounts="reReadAllAccounts" />
      </div>

      <div v-if="showMainAccountsList">
        <mainAccountsList :accounts="accounts" :total-balance="totalBalance" :base-currency-code="baseCurrencyCode" />
      </div>

    </div>
  </main>
</template>

<style scoped lang="scss">

</style>