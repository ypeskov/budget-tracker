<script setup>
import { onBeforeMount, reactive, ref } from 'vue';

import { Services } from '@/services/servicesConfig';
import BudgetsList from '@/components/budgets/BudgetsList.vue';
import BudgetNewComponent from '@/components/budgets/BudgetNewComponent.vue';

let budgets = reactive([]);

onBeforeMount(async () => {
  const response = await Services.budgetsService.getUserBudgets();
  budgets.length = 0;
  budgets.push(...response);
});

const showBudgetModal = ref(false);

const openBudgetModal = () => {
  showBudgetModal.value = true;
};

const closeBudgetModal = () => {
  showBudgetModal.value = false;
};
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col-2">
          <button class="btn btn-primary w-100"
                  @click="openBudgetModal">{{ $t('buttons.newBudget') }}</button>
          <teleport to="body">
            <BudgetNewComponent v-if="showBudgetModal" :close-modal="closeBudgetModal" />
          </teleport>
        </div>
      </div>

      <div class="row">
        <BudgetsList :budgets="budgets" />
      </div>
    </div>
  </main>
</template>

<style scoped>

</style>