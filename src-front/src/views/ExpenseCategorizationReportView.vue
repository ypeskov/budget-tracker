<script setup>
import { onBeforeMount, ref } from 'vue';
import { useRouter } from 'vue-router';
import { DateTime } from 'luxon';
import { processError } from '@/errors/errorHandlers';
import { Services } from '@/services/servicesConfig';

const router = useRouter();

const startDate = ref(DateTime.now().startOf('month').toISODate());
const endDate = ref(DateTime.now().toISODate());
const loading = ref(false);
const analysis = ref('');

onBeforeMount(async () => {
  try {
    await getReportData();
  } catch (e) {
    await processError(e, router);
  }
});

async function getReportData() {
  if (startDate.value === '' || endDate.value === '') {
    return;
  }

  loading.value = true;
  try {
    const response = await Services.reportsService.getAnalyticsReport('expense-categorization', {
      startDate: startDate.value,
      endDate: endDate.value
    });
    
    if (response.status === 'success') {
      analysis.value = response.analysis;
    }
  } catch (e) {
    await processError(e, router);
  } finally {
    loading.value = false;
  }
}

async function changeDate() {
  if (startDate.value !== '' && endDate.value !== '') {
    await getReportData();
  }
}
</script>

<template>
  <div class="section-card">
    <h2>{{ $t('message.expenseCategorizationReport') }}</h2>

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
    </div>

    <div v-if="loading" class="text-muted" style="margin-top: 20px; text-align: center;">
      {{ $t('message.loading') }}...
    </div>

    <div v-else-if="analysis" class="analysis-content" style="margin-top: 20px;">
      <div v-html="analysis"></div>
    </div>

    <div v-else class="text-muted" style="margin-top: 20px;">
      {{ $t('message.noData') }}
    </div>
  </div>
</template>

<style scoped>
.analysis-content {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  line-height: 1.6;
}

.analysis-content :deep(h2) {
  color: #495057;
  margin-bottom: 16px;
  font-size: 1.5rem;
}

.analysis-content :deep(h3) {
  color: #6c757d;
  margin-top: 20px;
  margin-bottom: 12px;
  font-size: 1.2rem;
}

.analysis-content :deep(p) {
  margin-bottom: 12px;
}

.analysis-content :deep(ul) {
  margin-bottom: 16px;
  padding-left: 20px;
}

.analysis-content :deep(li) {
  margin-bottom: 8px;
}

.analysis-content :deep(strong) {
  color: #495057;
  font-weight: 600;
}
</style>