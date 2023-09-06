<script setup>
import { onBeforeMount, reactive } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import {AccountService} from '../services/accounts';

let accounts = reactive([]);
const accService = new AccountService();
const router = useRouter();

onBeforeMount(async () => {
  try {
    accounts.length = 0;
    accounts.push(...await accService.getAllUserAccounts()); 
  } catch(e) {
    console.log(e.message);
    router.push({name: 'login'})
  }  
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
        <div v-for="acc in accounts" :key="acc.id" class="list-item">
          <RouterLink :to="{name: 'accountDetails', params: {id: acc.id}}">
            <div class="row">
              <div class="col">
              {{ acc.name }}
              </div>
              <div class="col">
                {{ acc.balance }}
              </div>
            </div>
          </RouterLink>
          
        </div>
    </div>
  </main>
</template>