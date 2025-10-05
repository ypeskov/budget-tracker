<template>
  <div class="upcoming-transactions-list">
    <div v-if="groupedTransactions.length === 0" class="empty-state">
      <i class="bi bi-calendar-check display-1 text-muted mb-3"></i>
      <p class="text-muted">{{ $t('financialPlanning.noPlannedTransactions') }}</p>
    </div>

    <div v-for="group in groupedTransactions" :key="group.date" class="transaction-group">
      <div class="group-header" :class="group.class">
        <i :class="group.icon"></i>
        <span class="group-title">{{ group.title }}</span>
        <span class="group-count">{{ group.transactions.length }}</span>
      </div>

      <div class="transactions-list">
        <div
          v-for="transaction in group.transactions"
          :key="`${transaction.plannedTransactionId}-${transaction.occurrenceDate}`"
          class="transaction-card"
          :class="{ overdue: group.isOverdue }"
        >
          <div class="transaction-icon" :class="transaction.isIncome ? 'income' : 'expense'">
            <i :class="transaction.isIncome ? 'bi bi-arrow-up-circle' : 'bi bi-arrow-down-circle'"></i>
          </div>

          <div class="transaction-info">
            <div class="transaction-header">
              <span class="transaction-label">{{ transaction.label || $t('common.noLabel') }}</span>
            </div>
            <div class="transaction-details">
              <span class="transaction-date">
                <i class="bi bi-calendar3"></i>
                {{ formatDate(transaction.occurrenceDate) }}
              </span>
            </div>
          </div>

          <div class="transaction-amount" :class="transaction.isIncome ? 'income' : 'expense'">
            <span class="amount-value">
              {{ transaction.isIncome ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
            </span>
          </div>

          <div class="transaction-actions">
            <i
              @click="$emit('edit', transaction.plannedTransactionId)"
              class="fa-solid fa-pen-to-square action-icon edit-icon"
              :title="$t('common.edit')"
            ></i>
            <i
              @click="$emit('delete', transaction.plannedTransactionId)"
              class="fa-solid fa-trash-can action-icon delete-icon"
              :title="$t('common.delete')"
            ></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const props = defineProps({
  transactions: {
    type: Array,
    required: true,
  },
  currency: {
    type: String,
    default: 'USD',
  },
});

defineEmits(['edit', 'delete']);

const groupedTransactions = computed(() => {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const today = new Date(now);
  const tomorrow = new Date(now);
  tomorrow.setDate(tomorrow.getDate() + 1);
  const nextWeek = new Date(now);
  nextWeek.setDate(nextWeek.getDate() + 7);

  const groups = {
    overdue: [],
    today: [],
    tomorrow: [],
    thisWeek: [],
    later: [],
  };

  props.transactions.forEach((tx) => {
    const txDate = new Date(tx.occurrenceDate);
    txDate.setHours(0, 0, 0, 0);

    if (txDate < today) {
      groups.overdue.push(tx);
    } else if (txDate.getTime() === today.getTime()) {
      groups.today.push(tx);
    } else if (txDate.getTime() === tomorrow.getTime()) {
      groups.tomorrow.push(tx);
    } else if (txDate < nextWeek) {
      groups.thisWeek.push(tx);
    } else {
      groups.later.push(tx);
    }
  });

  const result = [];

  if (groups.overdue.length > 0) {
    result.push({
      date: 'overdue',
      title: t('financialPlanning.overdue'),
      icon: 'bi bi-exclamation-triangle-fill',
      class: 'overdue',
      isOverdue: true,
      transactions: groups.overdue.sort((a, b) => new Date(a.occurrenceDate) - new Date(b.occurrenceDate)),
    });
  }

  if (groups.today.length > 0) {
    result.push({
      date: 'today',
      title: t('financialPlanning.today'),
      icon: 'bi bi-calendar-day',
      class: 'today',
      isOverdue: false,
      transactions: groups.today,
    });
  }

  if (groups.tomorrow.length > 0) {
    result.push({
      date: 'tomorrow',
      title: t('financialPlanning.tomorrow'),
      icon: 'bi bi-calendar',
      class: 'tomorrow',
      isOverdue: false,
      transactions: groups.tomorrow,
    });
  }

  if (groups.thisWeek.length > 0) {
    result.push({
      date: 'thisWeek',
      title: t('financialPlanning.thisWeek'),
      icon: 'bi bi-calendar-week',
      class: 'this-week',
      isOverdue: false,
      transactions: groups.thisWeek.sort((a, b) => new Date(a.occurrenceDate) - new Date(b.occurrenceDate)),
    });
  }

  if (groups.later.length > 0) {
    result.push({
      date: 'later',
      title: t('financialPlanning.later'),
      icon: 'bi bi-calendar-range',
      class: 'later',
      isOverdue: false,
      transactions: groups.later.sort((a, b) => new Date(a.occurrenceDate) - new Date(b.occurrenceDate)),
    });
  }

  return result;
});

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: props.currency,
  }).format(amount);
}
</script>

<style scoped>
.upcoming-transactions-list {
  margin-top: 2rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.transaction-group {
  margin-bottom: 2rem;
}

.group-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-radius: 8px 8px 0 0;
  font-weight: 600;
  font-size: 1rem;
}

.group-header.overdue {
  background: #fff3cd;
  color: #664d03;
}

.group-header.today {
  background: #d1ecf1;
  color: #0c5460;
}

.group-header.tomorrow {
  background: #e2e3e5;
  color: #383d41;
}

.group-count {
  margin-left: auto;
  background: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
}

.transactions-list {
  background: white;
  border: 1px solid #dee2e6;
  border-top: none;
  border-radius: 0 0 8px 8px;
}

.transaction-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #f1f3f5;
  transition: background-color 0.2s;
}

.transaction-card:last-child {
  border-bottom: none;
}

.transaction-card:hover {
  background-color: #f8f9fa;
}

.transaction-card.overdue {
  background-color: #fff9e6;
}

.transaction-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.transaction-icon.income {
  background-color: #d1f2eb;
  color: #198754;
}

.transaction-icon.expense {
  background-color: #f8d7da;
  color: #dc3545;
}

.transaction-info {
  flex: 1;
  min-width: 0;
}

.transaction-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.transaction-label {
  font-weight: 600;
  font-size: 1rem;
}

.recurring-badge {
  font-size: 0.75rem;
  background: #e7f1ff;
  color: #004085;
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.transaction-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.transaction-details > span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.transaction-amount {
  font-size: 1.25rem;
  font-weight: 700;
  min-width: 120px;
  text-align: right;
}

.transaction-amount.income {
  color: #198754;
}

.transaction-amount.expense {
  color: #dc3545;
}

.transaction-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.action-icon {
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-icon {
  color: #0d6efd;
}

.edit-icon:hover {
  color: #0a58ca;
  transform: scale(1.1);
}

.delete-icon {
  color: #dc3545;
}

.delete-icon:hover {
  color: #bb2d3b;
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .transaction-card {
    flex-wrap: wrap;
  }

  .transaction-info {
    width: 100%;
    order: 2;
  }

  .transaction-amount {
    order: 1;
    min-width: auto;
  }

  .transaction-actions {
    order: 3;
    width: 100%;
    justify-content: flex-end;
  }

  .transaction-details {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style>
