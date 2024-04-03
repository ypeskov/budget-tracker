<script setup>
import { computed, ref } from 'vue';

import { Services } from '../../services/servicesConfig';
import ModalWindow from '../utils/ModalWindow.vue';

const props = defineProps({
  closeModal: Function,
  category: Object,
  categories: Object,
});

const emits = defineEmits(['changeCategoryType', 'categoryUpdated']);

const isIncome = ref(props.category.isIncome);
const name = ref(props.category.name);
const parentId = ref(props.category.parentId);
const isDeleted = ref(props.category.isDeleted);

const showDeleteModal = ref(false);

const categoryOptions = computed(() => {
  return Object.values(props.categories).flat().map(cat => ({
    id: cat.id,
    name: cat.name,
  }));
});

const updateIsIncome = (newValue) => {
  isIncome.value = newValue;
  emits('changeCategoryType', { isIncome: newValue });
};

const saveCategory = async () => {
  const category = {
    name: name.value,
    isIncome: isIncome.value || false,
    isDeleted: isDeleted.value || false,
  };

  if (props.category.id) {
    category.id = props.category.id;
  }
  if (parentId.value) {
    category.parentId = parentId.value;
  }
  if (category.id) {
    await Services.categoriesService.updateCategory(category);
  } else {
    await Services.categoriesService.createCategory(category);
  }
  emits('categoryUpdated');
  props.closeModal();
};

function promptDeleteCategory() {
  showDeleteModal.value = true;
}

async function confirmDeleteCategory() {
  await Services.categoriesService.deleteCategory(props.category.id);
  emits('categoryUpdated');
  props.closeModal();
  showDeleteModal.value = false;
}


</script>

<template>
  <ModalWindow :close-modal="closeModal">
    <template #header>
      <h2>{{ $t('message.category') }}</h2>
    </template>

    <template #main>
      <div class="row mb-3">
        <div class="col">
          <label for="categoryName">{{ $t('message.name') }}</label>
          <input type="text" id="categoryName" class="form-control" v-model="name">
        </div>
        <div v-if="category.children.length === 0" class="col">
          <label for="categoryParent">{{ $t('message.group') }}</label>
          <select id="categoryParent" class="form-control" v-model="parentId">
            <option value="">{{ $t('message.none') }}</option>
            <option v-for="cat in categoryOptions" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col">
          <label>
            <input type="checkbox"
                   v-model="isIncome"
                   @change="updateIsIncome($event.target.checked)">{{ $t('message.isIncome') }}
          </label>
        </div>
        <div class="col">
          <label><input type="checkbox" v-model="isDeleted"> {{ $t('message.isDeleted') }}</label>
        </div>
      </div>

      <div class="row">
        <button class="btn btn-primary" @click="saveCategory">{{ $t('buttons.save') }}</button>
        <button class="btn btn-danger" @click="promptDeleteCategory">{{ $t('buttons.delete') }}</button>
      </div>
    </template>
  </ModalWindow>

  <ModalWindow :close-modal="() => showDeleteModal = false" v-if="showDeleteModal">
    <template #header>
      <h2>{{ $t('message.deleteCategory') }}?</h2>
    </template>

    <template #main>
      <p>{{ $t('message.areYouSureWantDeleteCategory') }}?</p>
      <div class="row gap-2 justify-content-center">
        <button class="btn btn-danger col-auto" @click="confirmDeleteCategory">{{ $t('buttons.delete') }}</button>
      </div>
    </template>
  </ModalWindow>

</template>

<style scoped>
.btn-primary, .btn-danger {
  margin-top: 10px;
}
</style>
