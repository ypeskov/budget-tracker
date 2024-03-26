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
            {{ $t('message.welcome') }}, {{ userStore.user.first_name }} {{ userStore.user.last_name }}
          </div>
          <div v-else>
            <RouterLink :to="{name: 'login'}">{{ $t('menu.login') }}</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
