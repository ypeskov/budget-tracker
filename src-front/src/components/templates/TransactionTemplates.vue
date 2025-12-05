<script setup>
import { ref, onBeforeMount, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { Services } from '@/services/servicesConfig';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const { t }     = useI18n();

const selectedTemplates = ref([]);
const filtered          = ref([]);
const query             = ref('');

onBeforeMount(async () => {
  const data = await Services.transactionsService.getUserTemplates();
  userStore.transactionTemplates.splice(0, userStore.transactionTemplates.length, ...data);
  filtered.value = userStore.transactionTemplates;
});

watch(query, v => {
  filtered.value = userStore.transactionTemplates.filter(t =>
    t.label.toLowerCase().includes(v.toLowerCase())
  );
});

async function remove() {
  await Services.transactionsService.deleteUserTemplates(selectedTemplates.value);
  const upd = await Services.transactionsService.getUserTemplates();
  userStore.transactionTemplates = upd;
  selectedTemplates.value = [];
  query.value = '';
}
</script>

<template>
  <div class="section-card templates-wrapper">
    <h3>{{ t('message.templates') }}</h3>

    <input
      v-model="query"
      class="form-control search"
      :placeholder="t('message.searchTemplates')"
    />

    <div class="tmpl-list">
      <label
        v-for="tpl in filtered"
        :key="tpl.id"
        class="tmpl-item"
      >
        <input
          type="checkbox"
          :value="tpl.id"
          v-model="selectedTemplates"
        />
        <span>{{ tpl.label }} <b>({{ tpl.category?.name }})</b></span>
      </label>
    </div>

    <button
      class="btn btn-primary"
      :disabled="!selectedTemplates.length"
      @click="remove"
    >
      {{ t('buttons.delete') }}
    </button>
  </div>
</template>

<style scoped>
.search { margin: 0 0 16px; }
.tmpl-list {
  display: flex; flex-direction: column;
  gap: 10px; max-height: 300px; overflow-y: auto;
  margin-bottom: 16px;
}
.tmpl-item { display: flex; align-items: center; gap: 8px; }
</style>
