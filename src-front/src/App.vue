<script setup>
import { RouterLink, RouterView } from 'vue-router'
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
              <RouterLink to="/">Home</RouterLink>
              <RouterLink to="/about">About</RouterLink>
              <RouterLink to="/login">Login</RouterLink>
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
