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
    <div v-for="budget in props.budgets" :key="budget.id">
      <div class="budget-item-container" @click="budgetSelected(budget)">
        <span class="col-4">{{ budget.name }} ({{ budget.currency.code }})</span>
        <span class="col-1">{{ $n(budget.collectedAmount, 'decimal') }}</span>
        <span class="col-1">{{ $n(budget.targetAmount, 'decimal') }}</span>
        <span class="col-1">{{ budget.period }}</span>
        <span class="col-1">{{ formatDate(budget.startDate) }}</span>
        <span class="col-1">{{ formatDate(budget.endDate) }}</span>
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
</style>