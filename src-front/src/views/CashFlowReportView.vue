<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { Bar } from 'vue-chartjs';
import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Title, Tooltip } from 'chart.js';

import { Services } from '@/services/servicesConfig';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const loaded = ref(false);

const chartData = reactive({
  labels: [],
  datasets: [
    {
      label: 'Total Income',
      backgroundColor: 'rgba(72,234,12,0.83)',
      data: [],
    },
    {
      label: 'Total Expenses',
      backgroundColor: 'rgba(245,28,70,0.83)',
      data: [],
    },
    {
      label: 'Net Flow',
      backgroundColor: 'rgba(12,53,199,0.82)',
      data: [],
    },
  ],
});

const chartOptions = reactive({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
    },
  },
});

const accounts = reactive([]);
const accountIdx = ref(0);

onBeforeMount(async () => {
  accounts.push(...(await Services.accountsService.getAllUserAccounts()));
  await getAccountData(accounts[accountIdx.value].id);
});

async function getAccountData(accountId) {
  const cashFlowReport = await Services.reportsService
    .getReport('cashflow', {
      accountIds: [accountId],
      period: 'monthly',
    });
  cashFlowReport.forEach(item => {
    chartData.labels.push(item.period + ' (' + item.accountName + ')');
    chartData.datasets[0].data.push(item.totalIncome);
    chartData.datasets[1].data.push(-1 * item.totalExpenses);  // Change sign to show expenses as negative values
    chartData.datasets[2].data.push(item.netFlow);
  });
  loaded.value = true;
}

function clearChartData() {
  chartData.labels = [];
  chartData.datasets[0].data = [];
  chartData.datasets[1].data = [];
  chartData.datasets[2].data = [];
}

async function changeAccount($event) {
  accountIdx.value = parseInt($event.target.value, 10);
  loaded.value = false;
  clearChartData();
  await getAccountData(accounts[$event.target.value].id);
  accountIdx.value = parseInt($event.target.value, 10);
}

</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <h1>{{ $t('message.cashFlowReport') }}</h1>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <select class="form-select bottom-space"
                  @change="changeAccount"
                  :value="accountIdx">
            <option v-for="(acc, index) in accounts" :key="acc.id" :value="index">
              {{ acc.name }}
            </option>
          </select>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <Bar v-if="loaded" :data="chartData" :options="chartOptions" />
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.row {
  margin: 1rem 1rem;
}
</style>