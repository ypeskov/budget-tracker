<script setup>
import { ref, watch } from 'vue';
import { useUserStore } from '@/stores/user';
import debounce from 'lodash/debounce';

const props = defineProps(['transaction']);
const emit = defineEmits(['update:label']);

const userStore = useUserStore();
const label = ref(props.transaction.label || '');
const suggestions = ref([]);

const filterSuggestions = debounce(() => {
  if (!label.value.trim() || label.value.length < 3) {
    suggestions.value = [];
    return;
  }
  const searchTerm = label.value.toLowerCase();
  suggestions.value = userStore.transactionTemplates
    .filter(t => t.label.toLowerCase().includes(searchTerm));
}, 500);

function selectSuggestion(selectedTemplate) {
  label.value = selectedTemplate.label;
  emit('update:label', selectedTemplate);
  suggestions.value = [];
}

watch(() => props.transaction.label, (newLabel) => {
  label.value = newLabel;
});

function labelChanged($event) {
  label.value = $event.target.value;
  emit('update:label', label.value);
  filterSuggestions();
}

</script>

<template>
  <div class="mb-3 position-relative">
    <label for="label" class="form-label">{{ $t('message.label') }}</label>
    <input type="text" class="form-control" @input="labelChanged" id="label" :value="label" autocomplete="off" />

    <ul v-if="suggestions.length" class="list-group position-absolute w-100 mt-1 shadow">
      <li v-for="suggestion in suggestions" :key="suggestion.label" class="list-group-item list-group-item-action"
        @click="selectSuggestion(suggestion)">
        {{ suggestion.label }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.position-relative {
  position: relative;
}

.list-group {
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}
</style>