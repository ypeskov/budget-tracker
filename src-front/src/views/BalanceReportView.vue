<script setup>
import { onBeforeMount, reactive, ref, watch } from 'vue';
import { DateTime } from 'luxon';

import { Services } from '@/services/servicesConfig';
import BalancesList from '@/components/reports/BalancesList.vue';

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
  const userAccounts = await Services.accountsService.getUserAccounts();
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
  <main>
    <div class="container">
      <div class="row mb-3 nowrap-row">
        <div class="col-12 col-md-6">
          <div class="form-group">
            <label for="prev-balance-date">{{ $t('message.prevDate') }}</label>
            <input id="prev-balance-date"
                   type="date"
                   class="form-control"
                   v-model="prevDate" />
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="form-group">
            <label for="current-balance-date">{{ $t('message.currentDate') }}</label>
            <input id="current-balance-date"
                   type="date"
                   class="form-control"
                   v-model="currentDate" />
          </div>
        </div>
      </div>

      <div class="row nowrap-row">
        <div class="col-12 col-md-6 mb-3 mb-md-0">
          <BalancesList :balance-data="prevBalanceData"
                        :base-currency-code="currentBalanceData[0]?.baseCurrencyCode || '---'"
                        :total-balance="totalPrevBalance"/>
        </div>
        <div class="col-12 col-md-6">
          <BalancesList :balance-data="currentBalanceData"
                        :base-currency-code="currentBalanceData[0]?.baseCurrencyCode || '---'"
                        :total-balance="totalCurrentBalance" />
        </div>
      </div>
    </div>
  </main>
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
</style>