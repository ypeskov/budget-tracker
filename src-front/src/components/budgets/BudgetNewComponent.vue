<script setup>
import { defineProps, onBeforeMount, reactive, ref, watch } from 'vue';

import ModalWindow from '@/components/utils/ModalWindow.vue';
import CategoriesFilter from '@/components/filter/CategoriesFilter.vue';
import { useCategoriesStore } from '@/stores/categories';
import { Services } from '@/services/servicesConfig';

const props = defineProps({
  closeModal: Function,
  editBudget: Object,
});

const emit = defineEmits(['budgetCreated']);

let userCategories = useCategoriesStore().categories;
if (userCategories.length === 0) {
  Services.categoriesService.getUserCategories();
  userCategories = useCategoriesStore().categories;
}

// console.log(props.editBudget);

const budgetName = ref(props.editBudget ? props.editBudget.name : '');
let currency = reactive(props.editBudget ? props.editBudget.currency : {});
const targetAmount = ref(props.editBudget ? props.editBudget.targetAmount : 0);
const period = ref(props.editBudget ? props.editBudget.period : '');
const repeat = ref(props.editBudget ? props.editBudget.repeat : false);
const startDate = ref(props.editBudget ? props.editBudget.startDate : '');
const endDate = ref(props.editBudget ? props.editBudget.endDate : '');
const comment = ref(props.editBudget ? props.editBudget.comment : '');
const currencies = reactive([]);

let categories = reactive([]);
const showCategoriesModal = ref(false);

onBeforeMount(async () => {
  currencies.push(...(await Services.currenciesService.getAllCurrencies()));
});

watch(currencies, (newCurrencies) => {
  if (newCurrencies.length > 0 && props.editBudget) {
    const matchedCurrency = newCurrencies.find(c => c.id === props.editBudget.currency.id);
    if (matchedCurrency) {
      currency = matchedCurrency;
    }
  }
});

function openCategoriesModal() {
  showCategoriesModal.value = true;
}

function closeCategoriesModal() {
  showCategoriesModal.value = false;
}

function categoriesUpdated(selectedCategories) {
  categories.length = 0;
  userCategories.forEach((category) => {
    if (selectedCategories.includes(category.id)) {
      categories.push(category);
    }
  });
  showCategoriesModal.value = false;
}

function extractCategoriesIds(categories) {
  return categories.map((category) => category.id);
}

async function submitForm() {
  const createdBudget = await Services.budgetsService.createBudget({
    name: budgetName.value,
    currencyId: currency.id,
    targetAmount: targetAmount.value,
    period: period.value,
    repeat: repeat.value,
    startDate: startDate.value,
    endDate: endDate.value,
    comment: comment.value,
    categories: extractCategoriesIds(categories),
  });

  if (createdBudget) {
    emit('budgetCreated', createdBudget);
  }

  props.closeModal();
}

</script>

<template>
  <ModalWindow :close-modal="closeModal">
    <template #header>
      <div class="row">
        <h2>Create New Budget</h2>
      </div>
    </template>

    <template #main>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input type="text" class="form-control" id="name" v-model="budgetName" maxlength="100" required>
        </div>

        <div class="mb-3">
          <label for="currencyId" class="form-label">Select Currency</label>
          <select id="currency_id" class="form-control" v-model="currency" required>
            <option v-for="currency in currencies" :key="currency.id" :value="currency">
              {{ currency.name }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label for="target_amount" class="form-label">Target Amount</label>
          <input type="number" class="form-control" id="target_amount" v-model="targetAmount" step="0.01" required>
        </div>

        <div class="mb-3">
          <label for="period" class="form-label">Period</label>
          <select class="form-select" id="period" v-model="period" required>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
            <option value="custom">Custom</option>
          </select>
        </div>

        <div class="form-check form-switch mb-3">
          <input type="checkbox" class="form-check-input" id="repeat" v-model="repeat">
          <label class="form-check-label" for="repeat">Repeat</label>
        </div>

        <div class="mb-3">
          <label for="start_date" class="form-label">Start Date</label>
          <input type="date" class="form-control" id="start_date" v-model="startDate" required>
        </div>

        <div class="mb-3">
          <label for="end_date" class="form-label">End Date</label>
          <input type="date" class="form-control" id="end_date" v-model="endDate" required>
        </div>

        <div class="mb-3">
          <label for="categories" class="form-label">{{ $t('message.categories') }}</label>
          <div v-for="category in categories" :key="category.id">
            {{ category.name }}
          </div>
        </div>

        <div class="mb-3">
          <a href="#"
             class="btn btn-primary"
             @click.stop="openCategoriesModal">{{ $t('message.selectCategories')}}</a>
          <teleport to="body">
            <CategoriesFilter v-if="showCategoriesModal"
                              :close-modal="closeCategoriesModal"
                              :initial-categories="extractCategoriesIds(categories)"
                              @categories-updated="categoriesUpdated" />
          </teleport>
        </div>

        <div class="mb-3">
          <label for="comment" class="form-label">Comment</label>
          <textarea class="form-control" id="comment" v-model="comment" rows="3"></textarea>
        </div>

        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </template>
  </ModalWindow>
</template>

<style scoped>
@import '@/assets/common.scss';

.form-label {
  font-weight: bold;
}

</style>