<script setup>
import { onBeforeMount } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

import { useUserStore } from './stores/user';
import { UserService } from './services/users';

const userStore = useUserStore();
const userService = new UserService();

onBeforeMount(() => {
  let localStorageUser, isLoggedIn, accessToken;
  try {
    localStorageUser = JSON.parse(localStorage.getItem('user'));
    isLoggedIn = JSON.parse(localStorage.getItem('isLoggedIn'));
    accessToken = localStorage.getItem('accessToken');
  } catch(e) {
    userService.logOutUser();
  }
  
  if (isLoggedIn) {
    userStore.isLoggedIn = isLoggedIn;
    useUserStore.accessToken = accessToken;
    userService.setUser(localStorageUser, isLoggedIn, accessToken);
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
                <RouterLink :to="{name: 'home'}">Home</RouterLink>
              </span>
              
              <span v-if="userStore.isLoggedIn">
                <RouterLink :to="{name: 'accounts'}">Accounts</RouterLink>
              </span>
              
              <span v-if="!userStore.isLoggedIn">
                <RouterLink :to="{name: 'login'}">Login</RouterLink>
              </span>
              <span v-else>
                <RouterLink :to="{name: 'logout'}">Logout</RouterLink>
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
