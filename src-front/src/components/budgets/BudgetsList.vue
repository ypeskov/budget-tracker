<script setup>
const props = defineProps({
  budgets: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(['budgetSelected']);

const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

const budgetSelected = (budget) => {
  emit('budgetSelected', budget);
};
</script>

<template>
  <div>
    <div class="budget-item-container headers">
      <span class="col-4">{{ $t('message.name') }}</span>
      <span class="col-1">{{ $t('message.collectedExpenses') }}</span>
      <span class="col-1">{{ $t('message.targetBudget') }}</span>
      <span class="col-1">{{ $t('message.period') }}</span>
      <span class="col-1">{{ $t('message.startDate') }}</span>
      <span class="col-1">{{ $t('message.endDate') }}</span>
    </div>
    <div v-for="budget in props.budgets" :key="budget.id">
      <div class="budget-item-container" @click="budgetSelected(budget)">
        <span class="data-cell col-4">{{ budget.name }} ({{ budget.currency.code }})</span>
        <span class="data-cell col-1">{{ $n(budget.collectedAmount, 'decimal') }}</span>
        <span class="data-cell col-1">{{ $n(budget.targetAmount, 'decimal') }}</span>
        <span class="data-cell col-1">{{ budget.period }}</span>
        <span class="data-cell col-1 date-cell">{{ formatDate(budget.startDate) }}</span>
        <span class="data-cell col-1 date-cell">{{ formatDate(budget.endDate) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/common.scss';

.budget-item-container {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  border-radius: 0.5rem;
  margin: 0.5rem 0;
  background-color: $item-background-color;
}

.budget-item-container:hover {
  background-color: $item-hover-background-color;
  cursor: pointer;
}

.headers {
  font-weight: bold;
  color: #0000ff;
  background-color: #f0f0f0;
  text-align: center;
}

@media (max-width: 768px) {
  .headers span, .date-cell {
    writing-mode: vertical-lr;
    white-space: nowrap;
  }

  .budget-item-container span {
    text-align: left;
  }

  .budget-item-container span:not(:last-child) {
    margin-bottom: 0.5rem;
  }
}

@media (max-width: 480px) {
  .data-cell {
    writing-mode: vertical-lr;
    text-orientation: mixed;
    white-space: nowrap;
  }
}
</style>
