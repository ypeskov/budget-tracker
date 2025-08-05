<script setup>
import { onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { Services } from '@/services/servicesConfig';
import CategoryEditor from './CategoryEditor.vue';

const { t } = useI18n();

const cats = reactive({ income: [], expenses: [] });
const showEditor   = ref(false);
const editableCat  = ref({});
const catPool      = ref([]);

async function loadCats() {
  const grouped = await Services.categoriesService.getGroupedCategories();
  cats.income   = [...grouped.income].sort((a,b)=>a.name.localeCompare(b.name));
  cats.expenses = [...grouped.expenses].sort((a,b)=>a.name.localeCompare(b.name));
}
onMounted(loadCats);

function openEditor(cat = { children: [] }) {
  editableCat.value = cat;
  catPool.value = cat.isIncome ? cats.income : cats.expenses;
  showEditor.value = true;
}
function closeEditor()  { showEditor.value = false; }
async function updated() { await loadCats(); }
</script>

<template>
  <div class="section-card cat-card">

    <div class="cat-header">
      <h3>{{ t('message.categories') }}</h3>
      <button class="btn primary" @click="openEditor()">
        <i class="fa-solid fa-plus"></i>
        {{ t('buttons.addNewCategory') }}
      </button>
    </div>

    <div class="cat-groups">
      <div v-for="type in ['income','expenses']" :key="type" class="cat-group">
        <h4>{{ type === 'income' ? t('message.income') : t('message.expense') }}</h4>

        <ul class="cat-list">
          <li v-for="c in cats[type]" :key="c.id" class="cat-item">
            <button class="btn cat-btn" @click="openEditor(c)">
              {{ c.name }}
            </button>

            <ul v-if="c.children.length" class="cat-sub">
              <li v-for="sc in c.children" :key="sc.id">
                <button class="btn cat-btn sub" @click="openEditor(sc)">
                  {{ sc.name }}
                </button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>

  <CategoryEditor
    v-if="showEditor"
    :category="editableCat"
    :categories="catPool"
    @category-updated="updated"
    @change-category-type="() => {}"
    :close-modal="closeEditor"
  />
</template>
