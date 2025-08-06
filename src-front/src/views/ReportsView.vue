<!-- src/views/ReportsView.vue -->
<script setup>
import { shallowRef } from 'vue';
import { useI18n }    from 'vue-i18n';

/* ── отчёты (соседние файлы) ───────────────────────────── */
import CashFlowReport  from './CashFlowReportView.vue';
import BalanceReport   from './BalanceReportView.vue';
import ExpensesReport  from './ExpensesReportView.vue';

const { t } = useI18n();

/* список вкладок */
const tabs = [
  { id: 'cash',  icon: 'fa-rotate-right',   key: 'buttons.cashFlowReport', comp: CashFlowReport },
  { id: 'bal',   icon: 'fa-scale-balanced', key: 'buttons.balanceReport',  comp: BalanceReport  },
  { id: 'exp',   icon: 'fa-chart-pie',      key: 'buttons.expensesReport', comp: ExpensesReport }
];

/* первая вкладка открыта сразу */
const activeId   = shallowRef(tabs[0].id);
const ActiveComp = shallowRef(tabs[0].comp);

function changeTab(id) {
  if (id === activeId.value) return;
  const tab = tabs.find(t => t.id === id);
  if (tab) {
    activeId.value  = tab.id;
    ActiveComp.value = tab.comp;
  }
}
</script>

<template>
  <main class="settings-page">             <!-- та же обёртка, что и у Settings -->
    <div class="container split">

      <!-- ▸ боковое меню --------------------------------------------------- -->
      <aside class="sidebar">
        <h2 class="title">{{ t('menu.reports') }}</h2>

        <nav class="side-nav">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            class="btn side-btn"
            :class="{ active: tab.id === activeId }"
            @click="changeTab(tab.id)"
          >
            <i :class="['fa-solid', tab.icon]"></i>
            {{ t(tab.key) }}
          </button>
        </nav>
      </aside>

      <!-- ▸ контент -------------------------------------------------------- -->
      <section class="settings-content panel">
        <component :is="ActiveComp" />
      </section>

    </div>
  </main>
</template>

<style scoped>
/* боковые кнопки — чтобы иконка не прилипала к тексту */
.side-btn {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
