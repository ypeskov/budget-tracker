<script setup>
const props = defineProps({
  budgets: {
    type: Array,
    required: true,
  },
});

const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

</script>

<template>
  <div>
    <div v-for="budget in props.budgets" :key="budget.id">
      <div class="budget-item-container">
        <span class="col-6">{{ budget.name }}</span>
        <span class="col-1">{{ budget.collected_amount }}</span>
        <span class="col-1">{{ budget.target_amount }}</span>
        <span class="col-1">{{ budget.period }}</span>
        <span class="col-1">{{ formatDate(budget.start_date) }}</span>
        <span class="col-1">{{ formatDate(budget.end_date) }}</span>
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