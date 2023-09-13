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

function changeCategory($event) {
  props.transaction.category_id = props.categories[$event.target.value].id;
}
</script>

<template>
  <label for="short_description" class="form-label">
    Category
  </label>
  <select class="form-select bottom-space" @change="changeCategory">
    <option v-for="(cat, index) in categories" :key="cat.id" :selected="index===0" :value="index">
      {{ cat.name }}
    </option>
  </select>
</template>
