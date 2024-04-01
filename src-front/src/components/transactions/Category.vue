<script setup>
import { defineProps, defineEmits } from 'vue';

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

</script>

<template>
  <label for="category-select" class="form-label">
    {{ $t('message.category') }}
  </label>
  <select id="category-select" class="form-select bottom-space" @change="changeCategory"
          :value="props.transaction.categoryId">
    <option v-for="category in categories" :key="category.id" :value="category.id">
      {{ categoryLabel(category) }}
    </option>
  </select>
</template>
