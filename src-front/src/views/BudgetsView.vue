<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

import { Services } from '@/services/servicesConfig';
import { processError } from '@/errors/errorHandlers';
import BudgetsList from '@/components/budgets/BudgetsList.vue';
import BudgetNewComponent from '@/components/budgets/BudgetNewComponent.vue';

const router = useRouter();

let budgets = reactive([]);
let currentBudget = reactive({});

onBeforeMount(async () => {
  await fetchBudgets();
});

const fetchBudgets = async () => {
  try {
    const response = await Services.budgetsService.getUserBudgets();
    budgets.length = 0;
    budgets.push(...response);
  } catch (e) {
    await processError(e, router);
  }
};

const showBudgetModal = ref(false);

const openBudgetModal = () => {
  showBudgetModal.value = true;
};

const startCreateBudget = () => {
  currentBudget = {};
  openBudgetModal();
};

const closeBudgetModal = () => {
  showBudgetModal.value = false;
};

const budgetCreated = (budget) => {
  currentBudget = budget;
  fetchBudgets();
};

const editBudget = (budget) => {
  currentBudget = budget;
  openBudgetModal();
};
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col-3">
          <button class="btn btn-primary w-100"
                  @click="startCreateBudget">{{ $t('buttons.newBudget') }}
          </button>
        </div>
      </div>

      <div class="row">
        <BudgetsList :budgets="budgets" @budget-selected="editBudget" />
      </div>

      <teleport to="body">
        <BudgetNewComponent v-if="showBudgetModal"
                            @budget-created="budgetCreated"
                            @budget-deleted="fetchBudgets"
                            @budget-archived="fetchBudgets"
                            :edit-budget="currentBudget"
                            :close-modal="closeBudgetModal" />
      </teleport>
    </div>
  </main>
</template>

<style scoped lang="scss">

</style>