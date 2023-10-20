<script setup>
import { computed } from 'vue';

const props = defineProps(['transaction', 'categories', 'itemType']);

const filteredCategories = computed(() => {
  if (props.categories.length > 0) {
    props.transaction.category_id = props.categories[0].id;
  } else {
    props.transaction.category_id = null;
  }
  
  return filtered;
});

const selectedCategoryIdx = computed(() => {
  const index = props.categories.findIndex(cat => cat.id === props.transaction.category_id);

  if (index !== -1) {
    return index;
  } else {
    return 0;
  }
});

function changeCategory($event) {
  props.transaction.category_id = props.categories[$event.target.value].id;
}
</script>

<template>
  <label for="label" class="form-label">
    Category
  </label>
  <select class="form-select bottom-space" @change="changeCategory" :value="selectedCategoryIdx">
    <option v-for="(cat, index) in categories" :key="cat.id"  :value="index">
      {{ cat.name }}
    </option>
  </select>
</template>
