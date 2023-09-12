<script setup>
const props = defineProps(['transaction'])
</script>

<template>
<div class="mb-3">
  <label for="short_description" class="form-label">Label</label>
  <input type="text" class="form-control" v-model="transaction.short_description" id="short_description">
</div>
</template>