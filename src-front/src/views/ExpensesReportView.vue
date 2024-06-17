<script setup>

import { onBeforeMount, reactive, ref } from 'vue';
import { DateTime } from 'luxon';
import { RouterLink, useRouter } from 'vue-router';
import { processError } from '@/errors/errorHandlers';
import { Services } from '@/services/servicesConfig';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const userStore = useUserStore();

const startDate = ref(DateTime.now().startOf('month').toISODate()); // 'YYYY-MM-DD'
const endDate = ref(DateTime.now().toISODate()); // 'YYYY-MM-DD'
let expensesReportData = reactive({});

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

  const tmpData = await Services.reportsService.getReport('expenses-by-categories', filters);
  expensesReportData = Object.assign(expensesReportData, tmpData);
}

onBeforeMount(async () => {
  try {
    await getReportData();
  } catch (e) {
    await processError(e, router);
  }
});

async function changeDate() {
  if (startDate.value !== '' && endDate.value !== '') {
    await getReportData();
  }
}

</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col"><h1>{{ $t('buttons.expensesReport') }}</h1></div>
      </div>

      <div class="row">
        <div class="col">
          <div class="date-section">
            <div>
              <label for="transaction-date">{{ $t('message.startDate') }}</label>
              <input id="transaction-date"
                     type="date"
                     class="form-control"
                     v-model="startDate"
                     @change="changeDate" />
            </div>
            <div>
              <label for="transaction-date">{{ $t('message.endDate') }}</label>
              <input id="transaction-date"
                     type="date"
                     class="form-control"
                     v-model="endDate"
                     @change="changeDate" />
            </div>
          </div>

          <div class="report-section">
            <span style="display: none;">{{ sum = 0 }}</span>
            <div v-if="Object.keys(expensesReportData).length > 0">


              <div v-for="(category, idx) in expensesReportData" :key="category.id" class="category-item-container">
                <div v-if="category.isParent && idx > 0" class="prev-sum">
                  {{ $n(sum, 'decimal') }}&nbsp;{{ userStore.baseCurrency }}
                  <span style="display: none;">{{ sum = 0 }}</span>
                </div>

                <RouterLink class="row-category-expenses" :to="{
                  name: 'transactions',
                  query: {
                    categories: category.id,
                  }
                }">
                  <div class="data-transaction-container">
                    <div>
                      <span class="category-name">{{ category.name }}</span>
                    </div>
                    <div class="category-expense-amount">
                      <div class="category-expenses">{{ $n(parseFloat(category.totalExpenses), 'decimal') }}</div>
                      <div class="expenses-currency">{{ category.currencyCode ?? userStore.baseCurrency }}</div>
                    </div>


                  </div>
                </RouterLink>
                <span style="display: none;">{{ sum += parseFloat(category.totalExpenses) }}</span>
              </div>
            </div>
            <div v-else>
              <span>{{ $t('message.noData') }}</span>
            </div>
          </div>

        </div>

      </div>
    </div>
  </main>
</template>

<style scoped lang="scss">
@import '@/assets/common.scss';

.date-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
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