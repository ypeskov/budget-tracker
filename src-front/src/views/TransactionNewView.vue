<script setup>
import { onBeforeMount, reactive } from 'vue';
import { useRouter } from 'vue-router';

import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';
import { AccountService } from '../services/accounts';


const userStore = useUserStore();
const accountStore = useAccountStore();
const accountService = new AccountService(userStore, accountStore);
const router = useRouter();

const accounts = reactive([]);
const currentAccount = reactive({});
const transaction = reactive({});

function changeAccount($event) {
  currentAccount.value = accounts[$event.target.value];
}

onBeforeMount(async () => {
  try {
    accounts.length = 0;
    accounts.push(...await accountService.getAllUserAccounts());
    currentAccount.value = accounts[0];
  } catch (e) {
    console.log(e.message);
    router.push({ name: 'login' })
  }
});

function changeNotes($event) {
  transaction.long_description = $event.target.value;
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <form @submit.prevent>
            <div class="mb-3">
              <label for="short_description" class="form-label">Label</label>
              <input type="email" class="form-control" id="short_description" aria-describedby="emailHelp">
            </div>

            <div class="mb-3">
              <div class="row">
                <div class="col-10">
                  <label for="amount" class="form-label">Amount</label>
                  <input type="number" class="form-control" id="amount">
                </div>
                <div class="col-2 currency">{{ currentAccount.value?.currency?.code }}</div>
              </div>
            </div>
            
            <select class="form-select bottom-space" @change="changeAccount">
              <option v-for="acc, index in accounts" :key="acc.id" :value="index">{{ acc.name }}</option>
            </select>

            <div class="mb-3">
              <label for="notes" class="form-label">Notes</label>
              <textarea @change="changeNotes" 
                        class="form-control"
                        id="notes"
                        rows="3">{{ transaction?.long_description }}</textarea>
            </div>

            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.bottom-space {
  margin-bottom: 1rem;
}

.currency {
  align-self: flex-end;
}
</style>