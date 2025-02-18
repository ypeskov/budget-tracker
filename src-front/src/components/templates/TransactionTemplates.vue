<script setup>
import ModalWindow from '@/components/utils/ModalWindow.vue';
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';
import { Services } from '@/services/servicesConfig';
const userStore = useUserStore();

const props = defineProps({
  closeModal: Function,
});

const selectedTemplates = ref([]);

const handleTemplateSelection = (templateId) => {
  if (selectedTemplates.value.includes(templateId)) {
    selectedTemplates.value = selectedTemplates.value.filter(id => id !== templateId);
  } else {
    selectedTemplates.value.push(templateId);
  }
};

const deleteTemplates = async () => {
  await Services.transactionsService.deleteUserTemplates(selectedTemplates.value);
  const updatedTemplates = await Services.transactionsService.getUserTemplates();
  userStore.transactionTemplates = updatedTemplates;

  props.closeModal();
};

</script>

<template>
  <div>
    <ModalWindow :close-modal="closeModal">
      <template #header>
        <div class="row">
          <div class="col-12">
            <h2>{{ $t('message.templates') }}</h2>
          </div>
        </div>
      </template>

      <template #main>
        <div class="row">
          <div class="col-12">
            <div v-for="template in userStore.transactionTemplates" :key="template.id"
              @click="handleTemplateSelection(template.id)" class="list-item d-flex align-items-center gap-2">
              <input class="form-check-input" type="checkbox" :value="template.id" :id="'template-' + template.id">
              <label class="form-check-label" :for="'template-' + template.id">
                {{ template.label }} ({{ template.categoryId }})
              </label>
            </div>
          </div>

          <button class="btn btn-primary mt-4" @click="deleteTemplates">{{ $t('buttons.delete') }}</button>
        </div>
      </template>
    </ModalWindow>
  </div>
</template>