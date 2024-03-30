<script setup>
import { onBeforeMount, defineProps, reactive } from 'vue';

import { Services } from '../../services/servicesConfig';

const categories = reactive({});

defineProps({
  closeModal: Function,
});

onBeforeMount(async () => {
  const newCategories = await Services.categoriesService.getGroupedCategories();
  Object.keys(categories).forEach(key => delete categories[key]);
  Object.assign(categories, newCategories);
});

</script>

<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h2>{{ $t('message.categories') }}</h2>
      <div class="container">

        <div class="row">
          <div class="col-12">
            <h3>{{ 'Expenses' }}</h3>
            <ul>
              <li v-for="category in categories['expenses']" :key="category.id">
                {{ category.name }}
                <ul>
                  <li v-for="subCategory in category.children" :key="subCategory.id">
                    {{ subCategory.name }}
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>

        <div class="row">
          <div class="col-12">
            <h3>{{ 'Income' }}</h3>
            <ul>
              <li v-for="category in categories['income']" :key="category.id">
                {{ category.name }}
                <ul>
                  <li v-for="subCategory in category.children" :key="subCategory.id">
                    {{ subCategory.name }}
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>

        <div class="row">
          <button class="btn btn-secondary" @click="closeModal">{{ $t('buttons.close') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>

</style>