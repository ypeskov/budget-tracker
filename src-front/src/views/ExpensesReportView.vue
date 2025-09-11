<script setup>
import { onBeforeMount, reactive, ref, computed } from 'vue';
import { DateTime } from 'luxon';
import { RouterLink, useRouter } from 'vue-router';
import { Doughnut } from 'vue-chartjs';
import { ArcElement, CategoryScale, Chart as ChartJS, Legend, Title, Tooltip } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { processError } from '@/errors/errorHandlers';
import { Services } from '@/services/servicesConfig';
import { useUserStore } from '@/stores/user';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

const router = useRouter();
const userStore = useUserStore();

const startDate = ref(DateTime.now().startOf('month').toISODate());
const endDate = ref(DateTime.now().toISODate());
const hideEmptyCategories = ref(true);
let expensesReportData = reactive([]);

const pieChartData = reactive({
  labels: [],
  datasets: [{
    data: [],
    backgroundColor: [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
      '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
    ],
    borderWidth: 2,
    borderColor: '#fff'
  }]
});

const pieChartOptions = reactive({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        boxWidth: 12,
        padding: 15
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.label || '';
          const value = context.parsed;
          const total = context.dataset.data.reduce((a, b) => a + b, 0);
          const percentage = ((value / total) * 100).toFixed(1);
          return `${label}: ${percentage}% (${userStore.baseCurrency} ${value.toLocaleString()})`;
        }
      }
    },
    datalabels: {
      color: '#fff',
      font: {
        weight: 'bold',
        size: 14
      },
      formatter: function(value, context) {
        const total = context.dataset.data.reduce((a, b) => a + b, 0);
        const percentage = ((value / total) * 100).toFixed(1);
        return percentage >= 5 ? `${percentage}%` : ''; // Only show % if slice is >= 5%
      }
    }
  }
});

const aggregatedCategories = ref([]);
const aggregatedSum = ref(0);
const chartLoaded = ref(false);

const grouped = computed(() => {
  const res = [];
  let lastParent = null;
  let group = null;
  for (const c of expensesReportData) {
    const parent = c.parentId === null ? c.id : c.parentId;
    if (parent !== lastParent) {
      lastParent = parent;
      group = { parentId: parent, items: [], sum: 0 };
      res.push(group);
    }
    group.items.push(c);
    group.sum += parseFloat(c.totalExpenses);
  }
  return res;
});

async function getReportData() {
  const filters = { categories: [] };
  if (startDate.value !== '') {
    filters.startDate = startDate.value;
  }
  if (endDate.value !== '') {
    filters.endDate = endDate.value;
  }
  filters.hideEmptyCategories = hideEmptyCategories.value;
  const tmpData = await Services.reportsService.getReport('expenses-by-categories', filters);
  expensesReportData.splice(0);
  expensesReportData.push(...tmpData);
}

async function getDiagramData() {
  aggregatedCategories.value.splice(0);
  aggregatedCategories.value = await Services.reportsService.getReport('expenses-data', {
    startDate: startDate.value,
    endDate: endDate.value,
  });
  aggregatedSum.value = aggregatedCategories.value.reduce((acc, category) => acc + category.amount, 0);
}

onBeforeMount(async () => {
  try {
    await getReportData();
    await getDiagramData();
    await fetchPieDiagram();
  } catch (e) {
    await processError(e, router);
  }
});

async function fetchPieDiagram() {
  const start = startDate.value;
  const end = endDate.value;
  try {
    const diagramData = await Services.reportsService.getDiagram('pie', start, end);
    
    // Update Chart.js data
    pieChartData.labels = diagramData.labels;
    pieChartData.datasets[0].data = diagramData.data;
    
    chartLoaded.value = true;
  } catch (e) {
    await processError(e, router);
  }
}

async function changeDate() {
  if (startDate.value !== '' && endDate.value !== '') {
    chartLoaded.value = false;
    await getReportData();
    await getDiagramData();
    await fetchPieDiagram();
  }
}

async function changeHideEmptyCategories() {
  await getReportData();
}
</script>

<template>
  <div class="section-card">
    <h2>{{ $t('message.expensesReport') }}</h2>

    <div
      style="
        display: grid;
        gap: 16px;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        margin-top: 16px;
        align-items: end;
      "
    >
      <label>
        {{ $t('message.startDate') }}
        <input
          type="date"
          class="form-control"
          v-model="startDate"
          @change="changeDate"
        />
      </label>

      <label>
        {{ $t('message.endDate') }}
        <input
          type="date"
          class="form-control"
          v-model="endDate"
          @change="changeDate"
        />
      </label>

      <div class="hide-empty-categories form-check form-switch mb-3">
        <input
          class="form-check-input"
          type="checkbox"
          id="hide-empty-categories"
          v-model="hideEmptyCategories"
          @change="changeHideEmptyCategories"
        />
        <label class="form-check-label" for="hide-empty-categories">
          {{ $t('message.hideEmptyCategories') }}
        </label>
      </div>
    </div>

    <div
      v-if="aggregatedSum > 0"
      style="
        display: grid;
        gap: 16px;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        align-items: center;
        margin-top: 16px;
      "
    >
      <div class="diagram-img-container">
        <div v-if="chartLoaded && aggregatedSum > 0" style="height: 300px;">
          <Doughnut :data="pieChartData" :options="pieChartOptions" :plugins="[ChartDataLabels]" />
        </div>
        <div v-else-if="!chartLoaded">
          <span class="text-muted">{{ $t('message.loadingDiagram') }}</span>
        </div>
        <div v-else>
          <span class="text-muted">{{ $t('message.noData') }}</span>
        </div>
      </div>

      <div class="data-container" style="align-self:center">
        <ul class="list-group">
          <li
            v-for="category in aggregatedCategories"
            :key="category.id"
            class="list-group-item d-flex justify-content-between align-items-center"
            style="gap:12px"
          >
            <span>{{ category.label }}</span>

            <span style="display:inline-flex;align-items:center;gap:10px">
              <span
                style="
                  display:inline-block;min-width:44px;padding:2px 8px;
                  border-radius:999px;font-size:12px;text-align:center;
                  background:rgba(30,144,255,.12);color:#1e90ff;
                "
              >
                {{ ((category.amount * 100) / aggregatedSum).toFixed(1) }}%
              </span>
              <span>
                {{ $n(category.amount, 'decimal') }} {{ userStore.baseCurrency }}
              </span>
            </span>
          </li>

          <li class="list-group-item expenses-total d-flex justify-content-between align-items-center">
            <span>{{ $t('message.totalExpenses') }}</span>
            <span>{{ $n(aggregatedSum, 'decimal') }} {{ userStore.baseCurrency }}</span>
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="text-muted" style="margin-top:16px">
      {{ $t('message.noData') }}
    </div>
  </div>

  <div class="section-card" style="margin-top:16px">
    <div class="report-section">
      <div v-if="grouped.length">
        <div v-for="g in grouped" :key="g.parentId">
          <div v-for="category in g.items" :key="category.id" class="category-item-container">
            <RouterLink
              class="row-category-expenses"
              :to="{
                name: 'transactions',
                query: {
                  categories: category.id,
                  startDate: startDate,
                  endDate: endDate
                }
              }"
            >
              <div class="data-transaction-container">
                <div>
                  <span class="category-name">{{ category.name }}</span>
                </div>

                <div class="category-expense-amount">
                  <div class="category-expenses">
                    {{ $n(parseFloat(category.totalExpenses), 'decimal') }}
                  </div>
                  <div class="expenses-currency">
                    {{ category.currencyCode ?? userStore.baseCurrency }}
                  </div>
                </div>
              </div>
            </RouterLink>
          </div>

          <div class="prev-sum">
            {{ $n(g.sum, 'decimal') }}&nbsp;{{ userStore.baseCurrency }}
          </div>
        </div>
      </div>

      <div v-else>
        <span>{{ $t('message.noData') }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/common.scss' as *;

.date-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.diagram-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.diagram-img-container {
  flex: 0 0 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.data-container {
  flex: 0 0 50%;
}

.data-container ul {
  list-style-type: none;
  padding: 0;
}

.data-container li {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.expenses-total {
  border: 1px solid;
  font-weight: bold;
  background-color: $item-hover-background-color;
}

.prev-sum {
  text-align: right;
  font-weight: bold;
  margin-bottom: 15px;
  margin-right: 10px;
}

.data-transaction-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  border: 1px solid;
  border-radius: 5px;
  padding: 10px;
}

.row-category-expenses {
  text-decoration: none;
}

.data-transaction-container:hover {
  background-color: $item-hover-background-color;
}

.category-expense-amount {
  display: flex;
  justify-content: space-between;
}

.category-expense-amount > div {
  margin-right: 10px;
}
</style>
