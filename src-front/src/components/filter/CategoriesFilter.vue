<script setup>
import ModalWindow from '@/components/utils/ModalWindow.vue';
import { defineProps, reactive, ref } from 'vue';

import { useCategoriesStore } from '@/stores/categories';
import { Services } from '@/services/servicesConfig';

const props = defineProps({
  closeModal: Function,
  initialCategories: Array,
});

const emit = defineEmits(['categoriesUpdated']);

let userCategories = useCategoriesStore().categories;
if (userCategories.length === 0) {
  Services.categoriesService.getUserCategories();
  userCategories = useCategoriesStore().categories;
}

const selectedCategories = ref([...props.initialCategories])

function applyCategories() {
  emit('categoriesUpdated', selectedCategories.value);
}

function updateSelectedCategories(event) {
  const categoryId = parseInt(event.target.value);
  if (event.target.checked) {
    selectedCategories.value.push(categoryId);
  } else {
    const index = selectedCategories.value.indexOf(categoryId);
    selectedCategories.value.splice(index, 1);
  }
}

</script>

<template>
  <ModalWindow :close-modal="closeModal">
    <template #header>
      <div class="row">
        <h2>{{ $t('message.categories') }}</h2>
      </div>
    </template>

    <template #main>
      <div v-for="category in userCategories" :key="category.id" class="form-check form-switch">
        <input type="checkbox"
               class="form-check-input"
               :id="category.id"
               @change="updateSelectedCategories"
               v-model="selectedCategories"
               :value="category.id" />
        <label :for="category.id">{{ category.name }}</label>
      </div>
      <button class="btn btn-primary" @click="applyCategories">{{ $t('buttons.apply') }}</button>
    </template>
  </ModalWindow>

</template>

<style scoped lang="scss">

</style>