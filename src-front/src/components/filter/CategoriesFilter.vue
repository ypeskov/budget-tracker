<script setup>
import ModalWindow from '@/components/utils/ModalWindow.vue';
import { defineProps, reactive } from 'vue';
import { useCategoriesStore } from '@/stores/categories';

const props = defineProps({
  closeModal: Function,
  initialCategories: Array,
});

const emit = defineEmits(['categoriesUpdated']);

const userCategories = useCategoriesStore().categories;
const selectedCategories = reactive([...props.initialCategories])

function applyCategories() {
  emit('categoriesUpdated', selectedCategories);
}

function updateSelectedCategories(event) {
  const categoryId = parseInt(event.target.value);
  if (event.target.checked) {
    selectedCategories.push(categoryId);
  } else {
    const index = selectedCategories.indexOf(categoryId);
    selectedCategories.splice(index, 1);
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