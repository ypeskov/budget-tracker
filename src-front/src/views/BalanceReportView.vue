<script setup>
import { onBeforeMount, reactive, ref, watch } from 'vue';
import { DateTime } from 'luxon';
import { useRouter } from 'vue-router';

import { Services } from '@/services/servicesConfig';
import { processError } from '@/errors/errorHandlers';
import BalancesList from '@/components/reports/BalancesList.vue';

const router = useRouter();

const prevDate = ref('');
const currentDate = ref('');
const prevBalanceData = reactive([]);
const currentBalanceData = reactive([]);
const accounts = reactive([]);
const selectedAccountIds = reactive([17, 18, 19, 20, 31]);
const totalPrevBalance = ref(0);
const totalCurrentBalance = ref(0);

const updateBalanceData = async (balanceDate, balancesData, totalBalance) => {
  const data = await Services.reportsService.getReport('balance', {
    'account_ids': selectedAccountIds,
    'balanceDate': balanceDate.value,
  });
  balancesData.length = 0;
  balancesData.push(...data);

  totalBalance.value = balancesData.reduce((acc, item) => acc + item.baseCurrencyBalance, 0);
};

onBeforeMount(async () => {
  let userAccounts = [];
  try {
    userAccounts = await Services.accountsService.getUserAccounts({shouldUpdate: true});
  } catch (e) {
    await processError(e, router);
  }
  accounts.push(...userAccounts);
  selectedAccountIds.length = 0;
  selectedAccountIds.push(...userAccounts.map((account) => account.id));

  prevDate.value = DateTime.now().minus({ month: 1 }).toISODate();
  currentDate.value = DateTime.now().toISODate();
});

watch(prevDate, async (newVal) => {
  prevDate.value = DateTime.fromISO(newVal).toISODate();
  await updateBalanceData(prevDate, prevBalanceData, totalPrevBalance);
});

watch(currentDate, async (newVal) => {
  currentDate.value = DateTime.fromISO(newVal).toISODate();
  await updateBalanceData(currentDate, currentBalanceData, totalCurrentBalance);
});

</script>

<template>
  <div class="section-card">
    <h2>{{ $t('message.balanceReport') }}</h2>

    <div
      style="
        display:grid;
        gap:16px;
        grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
        margin-top:16px;
      "
    >
      <label>
        {{ $t('message.prevDate') }}
        <input
          id="prev-balance-date"
          type="date"
          class="form-control"
          v-model="prevDate"
        />
      </label>

      <label>
        {{ $t('message.currentDate') }}
        <input
          id="current-balance-date"
          type="date"
          class="form-control"
          v-model="currentDate"
        />
      </label>
    </div>
  </div>

  <div class="section-card" style="margin-top:16px">
    <div class="balances-grid">
      <div class="balance-panel">
        <BalancesList
          :balance-data="prevBalanceData"
          :base-currency-code="currentBalanceData[0]?.baseCurrencyCode || '---'"
          :total-balance="totalPrevBalance"
        />
      </div>

      <div class="balance-panel">
        <BalancesList
          :balance-data="currentBalanceData"
          :base-currency-code="currentBalanceData[0]?.baseCurrencyCode || '---'"
          :total-balance="totalCurrentBalance"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.nowrap-row {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
}

.col-12.col-md-6 {
  flex: 0 0 auto;
  width: 50%;
}

.balances-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  align-items: start;
}

.balance-panel {
  min-width: 0;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

@media (max-width: 576px) {
  .balances-grid { grid-template-columns: 1fr; }
}
</style>
