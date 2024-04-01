<script setup>
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps(['transaction', 'categories']);
const emit = defineEmits(['update:categoryId']);

function changeCategory($event) {
  emit('update:categoryId', $event.target.value);
}

const getParentCategoryLabel = (category) => {
  const parentCategory = props.categories.find(cat => cat.id === category.parentId);
  return parentCategory ? `${parentCategory.name} >> ` : '';
};

const categoryLabel = category => `${getParentCategoryLabel(category)} ${category.name}`;

const sortedCategories = computed(() => {
  return [...props.categories].sort((a, b) => {
    const labelA = categoryLabel(a);
    const labelB = categoryLabel(b);
    return labelA.localeCompare(labelB);
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
      {{ categoryLabel(category) }}
    </option>
  </select>
</template>
