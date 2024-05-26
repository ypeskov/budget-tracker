<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { DateTime } from 'luxon';
import { Bar } from 'vue-chartjs';
import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Title, Tooltip } from 'chart.js';

import { Services } from '@/services/servicesConfig';
import { processError } from '@/errors/errorHandlers';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const router = useRouter();
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
const rawData = reactive([]);

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
const startDate = ref('');
const endDate = ref(DateTime.now().toISODate()); // 'YYYY-MM-DD'
const period = ref('monthly');

onBeforeMount(async () => {
  accounts.push(...(await Services.accountsService.getUserAccounts()));
  try {
    await getAccountData(accounts[accountIdx.value].id);
  } catch (e) {
    await processError(e, router);
  }
});

async function updateChartData() {
  clearChartData();
  await getAccountData(accounts[accountIdx.value].id);
}

async function getAccountData(accountId) {
  const filters = {
    accountIds: [accountId],
    period: period.value,
  };
  if (startDate.value !== '') {
    filters.startDate = startDate.value;
  }
  if (endDate.value !== '') {
    filters.endDate = endDate.value;
  }
  const cashFlowReport = await Services.reportsService.getReport('cashflow', filters);
  cashFlowReport.forEach(item => {
    chartData.labels.push(item.period + ' (' + item.accountName + ')');
    chartData.datasets[0].data.push(item.totalIncome);
    chartData.datasets[1].data.push(-1 * item.totalExpenses);  // Change sign to show expenses as negative values
    chartData.datasets[2].data.push(item.netFlow);
  });
  rawData.push(...cashFlowReport);
  loaded.value = true;
}

function clearChartData() {
  rawData.splice(0);
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

async function changeDate() {
  loaded.value = false;
  await updateChartData();
  loaded.value = true;
}

async function changePeriod($event) {
  period.value = $event.target.value;
  loaded.value = false;
  await updateChartData();
  loaded.value = true;
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
              {{ acc.name }}, {{ acc.currency.code }}
            </option>
          </select>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <div class="form-group">
            <label for="transaction-date">{{ $t('message.startDate') }}</label>
            <input id="transaction-date"
                   type="date"
                   class="form-control"
                   v-model="startDate"
                   @change="changeDate" />
          </div>
        </div>

        <div class="col">
          <div class="form-group">
            <label for="transaction-date">{{ $t('message.endDate') }}</label>
            <input id="transaction-date"
                   type="date"
                   class="form-control"
                   v-model="endDate"
                   @change="changeDate" />
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <label>{{ $t('message.period') }}</label>
          <select class="form-select bottom-space" @change="changePeriod" :value="period">
            <option value="monthly">{{ $t('message.monthly') }}</option>
            <option value="daily">{{ $t('message.daily') }}</option>
          </select>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <Bar v-if="loaded" :data="chartData" :options="chartOptions" />
        </div>
      </div>

      <div class="row">
        <div class="col">
          <div class="period-item">
            <div class="period-cell table-header">{{ $t('message.period') }}</div>
            <div class="name-cell table-header">{{ $t('message.account') }}</div>
            <div class="income-cell table-header">{{ $t('message.totalIncome') }}</div>
            <div class="expense-cell table-header">{{ $t('message.totalExpenses') }}</div>
            <div class="net-flow-cell table-header">{{ $t('message.netFlow') }}</div>
          </div>
          <div class="period-item" v-for="(item, index) in rawData" :key="index">
            <div class="period-cell">{{ item.period }}</div>
            <div class="name-cell">{{ item.accountName }}</div>
            <div class="income-cell">{{ $n(item.totalIncome, 'decimal') }}</div>
            <div class="expense-cell">{{ $n(item.totalExpenses, 'decimal') }}</div>
            <div class="net-flow-cell">{{ $n(item.netFlow, 'decimal') }}</div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.row {
  margin: 1rem 1rem;
}
.period-item {
  display: flex;
  justify-content: space-between;
  margin: 0.5rem 0;
}

.period-item:hover {
  background-color: #f0f0f0;
}

.period-cell, .name-cell {
  text-align: left;
  width: 15%;
}

.income-cell, .expense-cell, .net-flow-cell {
  text-align: right;
  width: 15%;
}

.table-header {
  text-align: center;
  font-weight: bold;
  border-bottom: 2px solid black;
}
</style>