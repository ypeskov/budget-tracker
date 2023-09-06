<script setup>
import { onBeforeMount } from 'vue';
import { useUserStore } from '../stores/user';
const userStore = useUserStore();
const accessToken = userStore.accessToken;

async function getAccounts() {
  const accountsUrl = 'http://localhost:9000/accounts';
  const requestHeaders = {
    'Content-Type': 'application/json',
    'auth-token': accessToken
  };

  const response = await fetch(accountsUrl, {headers: requestHeaders});
  const data = await response.json();
  console.log(data);
}

onBeforeMount(async () => {
  await getAccounts();
});
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <h3>Your accounts</h3>
        </div>
      </div>
      <div class="row">
        <div class="col">

        </div>
      </div>
    </div>
  </main>
</template>