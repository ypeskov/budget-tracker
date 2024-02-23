<script setup>
import { onBeforeMount, reactive, ref, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import { Services } from '../../services/servicesConfig';
import { HttpError } from '../../errors/HttpError';
import { useUserStore } from '../../stores/user';
import Filter from '../filter/Filter.vue';
import List from './List.vue';

const props = defineProps(['accountId', 'isAccountDetails',]);

const userStore = useUserStore();
let transactions = reactive([]);
let filteredTransactions = reactive([]);

const router = useRouter();

const showFilter = ref(false);
const reset = ref(true);

const returnUrlName = ref("");

if (props.isAccountDetails) {
  returnUrlName.value = 'accountDetails';
} else {
  returnUrlName.value = 'transactions';
}

async function fetchTransactions() {
  try {
    transactions.splice(0);
    const allTransactions = await Services.transactionsService.getUserTransactions({ accountId: props.accountId });
    transactions.push(...allTransactions);
    filteredTransactions.push(...allTransactions);
  } catch (e) {
    if (e instanceof HttpError && e.statusCode === 401) {
      router.push({ name: 'login' });
      return;
    } else {
      console.log(e);
    }
    router.push({ name: 'home' });
  }
}

watch(() => props.accountId, (newAccountId) => {
  if (newAccountId) {
    fetchTransactions();
  }
});

onBeforeMount(async () => {
  if (!props.isAccountDetails) {
    fetchTransactions();
  }
});

async function reloadTransactions(event) {
  event.preventDefault();
  const allTransactions = await Services.transactionsService.getUserTransactions({ accountId: props.accountId });
  transactions.splice(0);
  transactions.push(...allTransactions);
  filteredTransactions.splice(0);
  filteredTransactions.push(...allTransactions);
  reset.value = true;
}

function toggleFilter(event) {
  event.preventDefault();
  showFilter.value = !showFilter.value;
}

function filterApplied(payload) {
  filteredTransactions.splice(0);
  filteredTransactions.push(...payload.filteredTransactions);
  reset.value = payload.resetStatus;
  showFilter.value = false;
}
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col sub-menu">
        <span v-if="userStore.isLoggedIn">
          <RouterLink class="btn btn-secondary" 
                    :to="{ 
                      name: 'transactionNew', 
                      query: {
                        returnUrl: returnUrlName,
                        accountId: props.accountId,
                      }
                    }">New
          </RouterLink>
        </span>
        <span>
          <a href="" class="btn btn-secondary" @click="reloadTransactions">Reload</a>
        </span>
        <span>
          <a href="" class="btn" :class="{ 'active-filter btn-success': !reset, 'btn-secondary': reset }"
            @click="toggleFilter">Filter</a>
        </span>
      </div>
    </div>
    <div class="row">
      <div class="col" v-show="showFilter">
        <Filter @filter-applied="filterApplied" :transactions="transactions" :resetstatus="reset"
          :is-account-details="props.isAccountDetails" />
      </div>
    </div>

    <div class="row">
      <div class="col">
        <h3>Your transactions</h3>
      </div>
    </div>
    <div class="row">
      <List :transactions="filteredTransactions" :account-id="props.accountId" :return-url="returnUrlName" />
    </div>
  </div>
</template>