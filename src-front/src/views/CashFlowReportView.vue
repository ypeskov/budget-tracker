<script setup>
import { onBeforeMount, ref } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

import { Services } from '@/services/servicesConfig';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Total Income',
      backgroundColor: 'rgba(72,234,12,0.83)',
      data: []
    },
    {
      label: 'Total Expenses',
      backgroundColor: 'rgba(245,28,70,0.83)',
      data: []
    },
    {
      label: 'Net Flow',
      backgroundColor: 'rgba(12,53,199,0.82)',
      data: []
    }
  ]
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true
    }
  }
});

const accountsData = [
  {
    "accountId": 17,
    "accountName": "DSK Main",
    "currency": "BGN",
    "totalIncome": 0.0,
    "totalExpenses": 3008.44,
    "netFlow": -3008.44,
    "period": "2024-03"
  },
  {
    "accountId": 17,
    "accountName": "DSK Main",
    "currency": "BGN",
    "totalIncome": 14313.44,
    "totalExpenses": 9655.0,
    "netFlow": 4658.44,
    "period": "2024-04"
  },
  {
    "accountId": 18,
    "accountName": "DSK Virtual",
    "currency": "BGN",
    "totalIncome": 0.0,
    "totalExpenses": 0.0,
    "netFlow": 0.0,
    "period": "2024-04"
  }
];

accountsData.forEach(item => {
  chartData.value.labels.push(item.period + ' (' + item.accountName + ')');
  chartData.value.datasets[0].data.push(item.totalIncome);
  chartData.value.datasets[1].data.push(item.totalExpenses);
  chartData.value.datasets[2].data.push(item.netFlow);
});

onBeforeMount(async () => {
  const cashFlowReport = await Services.reportsService
    .getReport('cashflow', {
      accountIds: [17, 18, 19],
      period: 'daily',
    });
  console.log(cashFlowReport);

});

</script>

<template>
  <main>
    <div>
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </main>
</template>

<style scoped>
.row {
  margin: 1rem 1rem;
}
</style>