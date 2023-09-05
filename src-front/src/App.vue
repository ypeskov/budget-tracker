<script setup>
import { onBeforeMount } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

import { useUserStore } from './stores/user';

const userStore = useUserStore();

onBeforeMount(() => {
  const localStorageUser = localStorage.getItem('user');
  if (localStorageUser) {
    userStore.setUser(JSON.parse(localStorageUser));
  }
});


</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col">Another Budgeter</div>
    </div>
    <div class="row">
      <div class="col">
        <header>
          <div class="wrapper">
            <nav>
              <span>
                <RouterLink to="/">Home</RouterLink>
              </span>
              
              <span>
                <RouterLink to="/about">About</RouterLink>
              </span>
              
              <span v-if="userStore.user.id == null">
                <RouterLink to="/login">Login</RouterLink>
              </span>
              <span v-else>
                <RouterLink to="/logout">Logout</RouterLink>
              </span>
              
            </nav>
          </div>
        </header>
      </div>
    </div>
  </div>
  

  <RouterView />
</template>

<style scoped>
nav a {
  margin: 0 0.2rem;
}
</style>
