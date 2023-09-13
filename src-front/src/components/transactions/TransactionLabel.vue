<script setup>
const props = defineProps(['transaction']);

props.transaction.short_description = '';

function labelChanged($event) {
  props.transaction.short_description = $event.target.value;
}
</script>

<template>
  <div class="mb-3">
    <label
      for="short_description"
      class="form-label">
      Label
    </label>
    <input
      type="text"
      class="form-control"
      @keyup="labelChanged"
      id="short_description" />
  </div>
</template>
