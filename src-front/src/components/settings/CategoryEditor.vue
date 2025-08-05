<script setup>
import { reactive, toRefs, ref } from 'vue';
import { useI18n }  from 'vue-i18n';
import { Services } from '@/services/servicesConfig';
import ModalWindow  from '@/components/utils/ModalWindow.vue';

const props = defineProps({
  closeModal  : Function,
  category    : Object,
  categories  : Array
});
const emit = defineEmits(['categoryUpdated']);
const { t } = useI18n();

const state = reactive({
  id        : props.category.id,
  name      : props.category.name || '',
  isIncome  : props.category.isIncome || false,
  isDeleted : props.category.isDeleted || false,
  parentId  : props.category.parentId || ''
});
const askDelete = ref(false);

const categoryOptions = props.categories.map(c => ({ id: c.id, name: c.name }));

async function save() {
  const dto = { ...toRefs(state), name: state.name, isIncome: state.isIncome,
                isDeleted: state.isDeleted, parentId: state.parentId || null };
  state.id ? await Services.categoriesService.updateCategory(dto)
           : await Services.categoriesService.createCategory(dto);
  emit('categoryUpdated'); props.closeModal();
}

function promptDelete() { askDelete.value = true; }

async function reallyDelete() {
  await Services.categoriesService.deleteCategory(state.id);
  emit('categoryUpdated'); props.closeModal();
}
</script>

<template>
  <ModalWindow :close-modal="props.closeModal">
    <template #header>
      <h2>{{ t('message.category') }}</h2>
    </template>

    <template #main>
      <div class="form-grid">
        <label>
          {{ t('message.name') }}
          <input v-model="state.name" type="text" class="form-input" />
        </label>

        <label v-if="!props.category.children?.length">
          {{ t('message.group') }}
          <select v-model="state.parentId" class="select-input">
            <option value="">{{ t('message.none') }}</option>
            <option v-for="opt in categoryOptions" :key="opt.id" :value="opt.id">
              {{ opt.name }}
            </option>
          </select>
        </label>

        <label class="chk">
          <input type="checkbox" v-model="state.isIncome" />
          {{ t('message.isIncome') }}
        </label>

        <label class="chk">
          <input type="checkbox" v-model="state.isDeleted" />
          {{ t('message.isDeleted') }}
        </label>
      </div>

      <div class="btn-row">
        <button class="btn primary"  @click="save">
          {{ t('buttons.save') }}
        </button>

        <button v-if="state.id" class="btn outline danger" @click="promptDelete">
          {{ t('buttons.delete') }}
        </button>
      </div>
    </template>
  </ModalWindow>

  <ModalWindow v-if="askDelete" class="confirm-modal" :close-modal="() => (askDelete = false)">
    <template #header>
      <h2>{{ t('message.deleteCategory') }}?</h2>
    </template>
    <template #main>
      <p>{{ t('message.areYouSureWantDeleteCategory') }}</p>
      <div class="btn-row">
        <button class="btn outline" @click="askDelete = false">
          {{ t('buttons.cancel') }}
        </button>
        <button class="btn danger"  @click="reallyDelete">
          {{ t('buttons.delete') }}
        </button>
      </div>
    </template>
  </ModalWindow>
</template>

<style scoped>
.form-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
  margin-bottom: 24px;
}
.form-input {
  width: 100%;
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid #ced4da;
  border-radius: 4px;
}

.chk { display: flex; align-items: center; gap: 8px; }

.btn-row { display: flex; gap: 16px; flex-wrap: wrap; }
.btn.danger      { color: #dc3545; border-color: #dc3545; }
.btn.danger:hover{ background: #dc3545; color: #fff; }
</style>
