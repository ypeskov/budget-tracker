<script setup>

import { onBeforeMount, reactive, ref } from 'vue';
import { DateTime } from 'luxon';
import { RouterLink, useRouter } from 'vue-router';
import { processError } from '@/errors/errorHandlers';
import { Services } from '@/services/servicesConfig';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const userStore = useUserStore();

const startDate = ref(DateTime.now().startOf('month').toISODate());
const endDate = ref(DateTime.now().toISODate());
const hideEmptyCategories = ref(true);
let expensesReportData = reactive([]);

let groupSum = 0;
let currentParentId = null;

const pieDiagram = ref('');
const aggregatedCategories = ref([]);
const aggregatedSum = ref(0);

function isNewGroup(category) {
  if (category.parentId === null) {
    currentParentId = category.id;
    return true;
  }

  if (currentParentId !== category.parentId) {
    currentParentId = category.parentId;
    return true;
  }

  return false;
}

function isStart(category) {
  if (expensesReportData[0].id === category.id) {
    return true;
  }

  return false;
}

function addGroupSum(category) {
  groupSum += parseFloat(category.totalExpenses);
}

function getCurrentGroupSum() {
  return groupSum;
}

function resetGroupSum() {
  groupSum = 0;
}

async function getReportData() {
  const filters = {
    categories: [],
  };
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
  groupSum = 0;
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
    await fetchPieDiagram();
    await getDiagramData();
  } catch (e) {
    await processError(e, router);
  }
});

async function fetchPieDiagram() {
  const start = startDate.value;
  const end = endDate.value;

  try {
    pieDiagram.value = await Services.reportsService.getDiagram('pie', start, end);
  } catch (e) {
    await processError(e, router);
  }
}

async function changeDate() {
  if (startDate.value !== '' && endDate.value !== '') {
    await getReportData();
    await fetchPieDiagram();
    await getDiagramData();
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
        <div v-if="pieDiagram">
          <img :src="pieDiagram.image" alt="No Diagram" class="img-fluid" />
        </div>
        <div v-else>
          <span class="text-muted">{{ $t('message.loadingDiagram') }}</span>
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
      <div v-if="Object.keys(expensesReportData).length > 0">
        <div
          v-for="(category) in expensesReportData"
          :key="category.id"
          class="category-item-container"
        >
          <div v-if="isNewGroup(category) && !isStart(category)" class="prev-sum">
            {{ $n(getCurrentGroupSum(), 'decimal') }}&nbsp;{{ userStore.baseCurrency }}
            {{ resetGroupSum() }}
            {{ addGroupSum(category) }}
          </div>
          <div v-else>
            {{ addGroupSum(category) }}
          </div>

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
          {{ $n(getCurrentGroupSum(), 'decimal') }}&nbsp;{{ userStore.baseCurrency }}
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
