<script setup>
import { RouterLink } from 'vue-router'
import { useUserStore } from '../stores/user';
const userStore = useUserStore();


</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <div v-if="userStore.user.id">
            Welcome, {{ userStore.user.firstName }} {{ userStore.user.lastName }}
          </div>
          <div v-else>
            <RouterLink :to="{name: 'login'}">Login</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
