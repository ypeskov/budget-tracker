<script setup>
import { ref } from 'vue';

import UserProfile from '@/components/settings/UserProfile.vue';
import CategoriesManager from '@/components/settings/CategoriesManager.vue';
import TransactionTemplates from '@/components/templates/TransactionTemplates.vue';

const showProfileModal = ref(false);
const showCategoriesModal = ref(false);
const showTemplatesModal = ref(false);

const openProfileModal = () => {
  showProfileModal.value = true;
};

const closeProfileModal = () => {
  showProfileModal.value = false;
};

const openCategoriesModal = () => {
  showCategoriesModal.value = true;
};

const closeCategoriesModal = () => {
  showCategoriesModal.value = false;
};

const openTemplatesModal = () => {
  showTemplatesModal.value = true;
};

const closeTemplatesModal = () => {
  showTemplatesModal.value = false;
};
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h1>{{ $t('message.settings') }}</h1>
        </div>
      </div>

      <div class="row">
        <div class="col-12 profile-section">
          <button @click="openProfileModal" class="btn btn-primary w-100">{{ $t('buttons.profile') }}</button>
        </div>
        <teleport to="body">
          <UserProfile v-if="showProfileModal" :close-modal="closeProfileModal" />
        </teleport>
      </div>

      <div class="row">
        <div class="col-12 profile-section">
          <button @click="openTemplatesModal" class="btn btn-primary w-100">{{ $t('buttons.templates') }}</button>
        </div>
        <teleport to="body">
          <TransactionTemplates v-if="showTemplatesModal" :close-modal="closeTemplatesModal" />
        </teleport>
      </div>

      <div class="row">
        <div class="col-12 profile-section">
          <button @click="openCategoriesModal" class="btn btn-primary w-100">{{ $t('buttons.categories') }}</button>
        </div>
        <teleport to="body">
          <CategoriesManager v-if="showCategoriesModal" :close-modal="closeCategoriesModal" />
        </teleport>
      </div>
    </div>
  </main>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;

}

.row {
  margin-top: 20px;
  margin-left: 0;
  width: 100%;
}
</style>