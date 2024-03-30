<script setup>
defineProps({
  closeModal: Function,
});


</script>

<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h2>{{ $t('message.categories') }}</h2>
      <div class="container">
        <div class="row">
          <button class="btn btn-secondary" @click="closeModal">{{ $t('buttons.close') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>