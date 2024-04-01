<script setup>
import { defineProps, onBeforeMount, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { Services } from '../../services/servicesConfig';
import CategoryEditor from './CategoryEditor.vue';

const { t } = useI18n();

const categories = reactive({});
const categoriesForEdit = ref([]);
const showCategoryEditor = ref(false);
const currentCategory = ref({});

defineProps({
  closeModal: Function,
});

onBeforeMount(async () => {
  reReadCategories();
});

function reReadCategories() {
  Services.categoriesService.getGroupedCategories().then(newCategories => {
    Object.keys(categories).forEach(key => delete categories[key]);
    Object.assign(categories, newCategories);
  });
}

const closeCategoryEditor = () => {
  showCategoryEditor.value = false;
};

const openCategoryEditor = (category) => {
  currentCategory.value = category;
  if (currentCategory.value.isIncome) {
    categoriesForEdit.value = categories.income;
  } else {
    categoriesForEdit.value = categories.expenses;
  }

  showCategoryEditor.value = true;
};

const showCategoryType = function(type) {
  return type === 'income' ? t('message.income') : t('message.expense');
};

const updateCategoryType = ({isIncome}) => {
  if (isIncome) {
    categoriesForEdit.value = categories.income;
  } else {
    categoriesForEdit.value = categories.expenses;
  }
};

const categoryUpdated = async () => {
  reReadCategories();
};
</script>

<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h2>{{ $t('message.categories') }}</h2>
      <div class="container">
        <div class="row mb-3" v-for="(categoriesList, type) in categories" :key="type">
          <div class="col-12">
            <h3 class="py-2">{{ showCategoryType(type) }}</h3>
            <ul class="list-group">
              <li v-for="category in categoriesList" :key="category.id" class="list-group-item py-2">
                <a @click="openCategoryEditor(category)" class="btn btn-info">{{ category.name }}</a>

                <ul class="list-unstyled ms-4">
                  <li v-for="subCategory in category.children" :key="subCategory.id" class="py-1">
                    <a class="btn btn-secondary btn-sm"
                       @click="openCategoryEditor(subCategory)">{{ subCategory.name }}</a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
        <div class="row">
          <button class="btn btn-secondary" @click="closeModal">{{ $t('buttons.close') }}</button>
        </div>
      </div>
    </div>
    <teleport to="body">
      <CategoryEditor v-if="showCategoryEditor"
                      @change-category-type="updateCategoryType"
                      @category-updated="categoryUpdated"
                      :category="currentCategory"
                      :categories="categoriesForEdit"
                      :close-modal="closeCategoryEditor" />
    </teleport>
  </div>
</template>


<style scoped>
.list-group-item {
  padding: 0.5rem 1.25rem;
}
</style>
