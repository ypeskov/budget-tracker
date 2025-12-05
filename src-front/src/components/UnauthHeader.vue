<script setup>
import { RouterLink } from 'vue-router'
import LanguageSwitcher from './LanguageSwitcher.vue'
</script>

<template>
  <div class="unauth-header">
    <RouterLink :to="{ name: 'home' }" class="logo">
      Orgfin.run
    </RouterLink>

    <LanguageSwitcher />
  </div>
</template>

<style scoped>
.unauth-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  z-index: 1000;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  text-decoration: none;
  transition: color 0.3s;
}

.logo:hover {
  color: #007bff;
}
</style>
