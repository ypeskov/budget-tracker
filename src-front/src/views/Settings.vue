<script setup>
import { ref } from 'vue'

const showProfileModal = ref(false)
const showLanguageModal = ref(false)

const openProfileModal = () => {
  showProfileModal.value = true
}

const openLanguageModal = () => {
  showLanguageModal.value = true
}

const closeProfileModal = () => {
  showProfileModal.value = false
}

const closeLanguageModal = () => {
  showLanguageModal.value = false
}
</script>

<template>
<main>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <h1>Settings</h1>
      </div>
    </div>

    <div class="row">
      <div class="col-12 profile-section">
        <a href="/settings/profile" class="btn btn-primary w-100">Profile</a>
      </div>
    </div>

    <div class="row">
      <div class="col-12 lang-section">
        <button @click="openLanguageModal" class="btn btn-primary w-100">{{$t('buttons.language')}}</button>
      </div>
    </div>
  </div>

  <!-- Language Modal -->
  <teleport to="body">
    <div v-if="showLanguageModal" class="modal-overlay" @click="closeLanguageModal">
      <div class="modal-content" @click.stop>
        <h2>Select Language</h2>
        <!-- Language options go here -->
        <button @click="closeLanguageModal">Close</button>
      </div>
    </div>
  </teleport>
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 500px;
}
</style>