<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';
import { AccountService } from '../services/accounts';
import { CategoriesService } from '../services/categories';
import TransactionTypeTabs from '../components/transactions/TransactionTypeTabs.vue';
import TransactionLabel from '../components/transactions/TransactionLabel.vue';
import TransactionAmount from '../components/transactions/TransactionAmount.vue';

const router = useRouter();
const userStore = useUserStore();
const accountStore = useAccountStore();
const accountService = new AccountService(userStore, accountStore);
const categoriesService = new CategoriesService(userStore);

const accounts = reactive([]);
const currentAccount = ref({});
const transaction = reactive({});
const categories = ref([]);
const currentCategory = ref({});

function changeAccount($event) {
  currentAccount.value = accounts[$event.target.value];
}

function changeCategory($event) {
  currentCategory.value = categories[$event.target.value];
}

onBeforeMount(async () => {
  try {
    accounts.length = 0;
    accounts.push(...await accountService.getAllUserAccounts());
    currentAccount.value = accounts[0];

    const cats = await categoriesService.getUserCategories();
    categories.value = cats;
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

            <TransactionTypeTabs :transaction="transaction" />

            <TransactionLabel :transaction="transaction" />

            <TransactionAmount :transaction="transaction" :current-account="currentAccount" />

            <select v-if="!transaction.is_transfer" class="form-select bottom-space" @change="changeCategory">
              <option v-for="cat, index in categories" :key="cat.id" :value="index">{{ cat.name }}</option>
            </select>

            <select class="form-select bottom-space" @change="changeAccount">
              <option v-for="acc, index in accounts" :key="acc.id" :value="index">{{ acc.name }}</option>
            </select>

            <select v-if="transaction.is_transfer" class="form-select bottom-space" @change="changeAccount">
              <option v-for="acc, index in accounts" :key="acc.id" :value="index">{{ acc.name }}</option>
            </select>

            <div class="mb-3">
              <label for="notes" class="form-label">Notes</label>
              <textarea @keyup="changeNotes" class="form-control" id="notes"
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

.top-space {
  margin-top: 1rem;
}
</style>