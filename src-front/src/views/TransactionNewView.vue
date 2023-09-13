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
import Category from '../components/transactions/Category.vue';
import Account from '../components/transactions/Account.vue';

const router = useRouter();
const userStore = useUserStore();
const accountStore = useAccountStore();
const accountService = new AccountService(userStore, accountStore);
const categoriesService = new CategoriesService(userStore);

const accounts = reactive([]);
const currentAccount = ref({});
const transaction = reactive({});
const categories = ref([]);

const itemType = ref('expense');
transaction.is_transfer = itemType.value === 'transfer';

function changeAccount(account) {
  currentAccount.value = account;
}

onBeforeMount(async () => {
  try {
    accounts.length = 0;
    accounts.push(...(await accountService.getAllUserAccounts()));
    categories.value = await categoriesService.getUserCategories();
  } catch (e) {
    console.log(e.message);
    router.push({ name: 'login' });
  }
});

function changeNotes($event) {
  transaction.long_description = $event.target.value;
}

function changeItemType(type) {
  itemType.value = type;
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <form @submit.prevent>
            <TransactionTypeTabs @type-changed="changeItemType" :transaction="transaction" :item-type="itemType" />

            <TransactionLabel :transaction="transaction" />

            <TransactionAmount :transaction="transaction" :current-account="currentAccount" />

            <Category v-if="!transaction.is_transfer" :item-type="itemType" :transaction="transaction"
              :categories="categories" />

            <Account :transaction="transaction" @account-changed="changeAccount" account-type="src" :accounts="accounts" />

            <Account v-if="transaction.is_transfer === true" account-type="target" :transaction="transaction"
              :accounts="accounts" />

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
