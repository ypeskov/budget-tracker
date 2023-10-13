<script setup>
const types = ['expense', 'income', 'transfer',]
</script>

<template>
  <select class="form-select bottom-space" @change="">
    <option v-for="type in types" :key="type" :value="type" >
      {{ type }}
    </option>
  </select>
</template>