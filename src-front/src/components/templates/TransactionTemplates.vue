<script setup>
  import ModalWindow from '@/components/utils/ModalWindow.vue';
  import { useUserStore } from '@/stores/user';
  import { ref, onBeforeMount, watch, onMounted } from 'vue';
  import { Services } from '@/services/servicesConfig';
  import 'bootstrap-icons/font/bootstrap-icons.css';

  const userStore = useUserStore();

  const props = defineProps({
    closeModal: Function,
  });

  const selectedTemplates = ref([]);
  const filteredTemplates = ref([]);
  const searchQuery = ref('');
  const searchInput = ref(null);

  onBeforeMount(async () => {
    const templates = await Services.transactionsService.getUserTemplates();
    userStore.transactionTemplates.splice(0, userStore.transactionTemplates.length, ...templates);
    filteredTemplates.value = userStore.transactionTemplates;
  });

  onMounted(() => {
    searchInput.value.focus();
  });

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

  watch(searchQuery, (newVal) => {
    filteredTemplates.value = userStore.transactionTemplates.filter(template =>
      template.label.toLowerCase().includes(newVal.toLowerCase())
    );
  });

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
          <div class="col-12 mb-3 position-relative">
            <input type="text"
                   class="form-control"
                   v-model="searchQuery"
                   :placeholder="$t('message.searchTemplates')"
                   ref="searchInput">
            <i v-if="searchQuery"
               class="bi bi-x-circle-fill position-absolute"
               style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer;"
               @click="searchQuery = ''; searchInput.focus()"></i>
          </div>
          
          <div class="col-12">
            <div v-for="template in filteredTemplates" :key="template.id"
                 class="list-item d-flex align-items-center gap-2">
              <input class="form-check-input"
                     type="checkbox"
                     :value="template.id"
                     :id="'template-' + template.id"
                     @change="handleTemplateSelection(template.id)">
              <label class="form-check-label"
                     :for="'template-' + template.id">{{ template.label }}
                <b>({{ template.category?.name }})</b></label>
            </div>
          </div>

          <button class="btn btn-primary mt-4" @click="deleteTemplates">{{ $t('buttons.delete') }}</button>
        </div>
      </template>
    </ModalWindow>
  </div>
</template>