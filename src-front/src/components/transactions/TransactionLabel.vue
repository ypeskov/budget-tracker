<script setup>
const props = defineProps(['transaction']);

props.transaction.label = '';

function labelChanged($event) {
  props.transaction.label = $event.target.value;
}
</script>

<template>
  <div class="mb-3">
    <label for="label" class="form-label">{{ $t('message.label') }}</label>
    <input type="text" class="form-control" @keyup="labelChanged" id="label" :value="transaction.label" />
  </div>
</template>
