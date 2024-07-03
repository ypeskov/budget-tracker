<script setup>
import { onBeforeMount, reactive } from 'vue';

import { Services } from '@/services/servicesConfig';
import BudgetsList from '@/components/budgets/BudgetsList.vue';

let budgets = reactive([]);

onBeforeMount(async () => {
  const response = await Services.budgetsService.getUserBudgets();
  budgets.length = 0;
  budgets.push(...response);
});

</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        Budgets Management
      </div>

      <div class="row">
        <BudgetsList :budgets="budgets" />
      </div>
    </div>
  </main>
</template>

<style scoped>

</style>