<script setup>
import { onBeforeMount, reactive, ref, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import { Services } from '../../services/servicesConfig';
import { processError } from '../../errors/errorHandlers';
import { useUserStore } from '../../stores/user';
import Filter from '../filter/TransactionsFilter.vue';
import ListOfTransactions from './ListOfTransactions.vue';

const props = defineProps(['accountId', 'isAccountDetails']);

const userStore = useUserStore();

let transactions = reactive([]);
let filteredTransactions = reactive([]);

const loading = ref(false);
const noMoreTransactions = ref(false);
const page = ref(1);
const perPage = ref(20);

const router = useRouter();

const showFilter = ref(false);
const reset = ref(true);

const returnUrlName = ref('');

if (props.isAccountDetails) {
  returnUrlName.value = 'accountDetails';
} else {
  returnUrlName.value = 'transactions';
}

async function fetchTransactions() {
  try {
    transactions.splice(0);
    filteredTransactions.splice(0);
    await loadMoreTransactions();
  } catch (e) {
    await processError(e, router);
  }
}

watch(() => props.accountId, (newAccountId) => {
  if (newAccountId) {
    fetchTransactions();
  }
});

onBeforeMount(async () => {
  if (!props.isAccountDetails) {
    await fetchTransactions();
  }
});

async function reloadTransactions(event) {
  event.preventDefault();
  page.value = 1;

  try {
    transactions.splice(0);
    filteredTransactions.splice(0);
    await loadMoreTransactions();
    reset.value = true;
  } catch (e) {
    await processError(e, router);
  }
}

function toggleFilter(event) {
  event.preventDefault();
  showFilter.value = !showFilter.value;
}

async function loadMoreTransactions() {
  if (loading.value || noMoreTransactions.value) return;
  loading.value = true;

  try {
    const newTransactions = await Services.transactionsService
      .getUserTransactions(page.value, perPage.value, { accountId: props.accountId });
    if (newTransactions.length < perPage.value) {
      noMoreTransactions.value = true;
    }

    transactions.push(...newTransactions);
    filteredTransactions.push(...newTransactions);
    page.value++;
  } catch (e) {
    await processError(e, router);
  } finally {
    loading.value = false;
  }
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
                    }">
            <img src="/images/icons/new-icon.svg"
                 :title="$t('message.new')"
                 :alt="$t('message.new')" />
          </RouterLink>
        </span>
        <span>
          <a href="" class="btn" :class="{ 'active-filter btn-success': !reset, 'btn-secondary': reset }"
             @click="toggleFilter">
            <img src="/images/icons/filter-icon.svg"
                 :title="$t('message.filter')"
                 :alt="$t('message.filter')" />
            </a>
        </span>
        <span>
          <a href="" class="btn btn-secondary" @click="reloadTransactions">
            <img src="/images/icons/refresh-icon.svg"
                 :title="$t('message.refresh')"
                 :alt="$t('message.refresh')" />
          </a>
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
        <h3>{{ $t('message.yourTransactions') }}</h3>
      </div>
    </div>
    <div class="row">
      <ListOfTransactions :transactions="filteredTransactions"
                          @load-more="loadMoreTransactions"
                          :account-id="props.accountId"
                          :return-url="returnUrlName" />
      <div v-if="loading" class="loading">Loading...</div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '../../assets/main.scss';

.loading {
  text-align: center;
  padding: 20px;
}
</style>
