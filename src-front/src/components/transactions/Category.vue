<script setup>
import { computed, defineProps, defineEmits } from 'vue';

const props = defineProps(['transaction', 'categories']);
const emit = defineEmits(['update:categoryId']);

const userLocale = navigator.language || 'en-US';

function changeCategory($event) {
  emit('update:categoryId', $event.target.value);
}

const getCategoryPath = (category, categories) => {
  let path = category.name;
  let currentCategory = category;

  while (currentCategory.parentId) {
    const parentCategory = categories.find(cat => cat.id === currentCategory.parentId);
    if (!parentCategory) break;
    path = `${parentCategory.name} >> ${path}`;
    currentCategory = parentCategory;
  }

  return path;
};

const sortedCategories = computed(() => {
  return [...props.categories].sort((a, b) => {
    const pathA = getCategoryPath(a, props.categories);
    const pathB = getCategoryPath(b, props.categories);
    return pathA.localeCompare(pathB, userLocale);
  });
});
</script>

<template>
  <label for="category-select" class="form-label">
    {{ $t('message.category') }}
  </label>
  <select id="category-select" class="form-select bottom-space" @change="changeCategory"
          :value="props.transaction.categoryId">
    <option v-for="category in sortedCategories" :key="category.id" :value="category.id">
      {{ getCategoryPath(category, props.categories) }}
    </option>
  </select>
</template>

