<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

import { useUserStore } from '../stores/user';
import { useAccountStore } from '../stores/account';
import { AccountService } from '../services/accounts';
import { CategoriesService } from '../services/categories';
import { TransactionsService } from '../services/transactions';
import { UserService } from '../services/users';
import TransactionTypeTabs from '../components/transactions/TransactionTypeTabs.vue';
import TransactionLabel from '../components/transactions/TransactionLabel.vue';
import TransactionAmount from '../components/transactions/TransactionAmount.vue';
import Category from '../components/transactions/Category.vue';
import Account from '../components/transactions/Account.vue';

const router = useRouter();
const userStore = useUserStore();
const accountStore = useAccountStore();
const userService = new UserService(userStore);
const accountService = new AccountService(userStore, accountStore);
const categoriesService = new CategoriesService(userStore);
const transactionsService = new TransactionsService(userService);

const accounts = reactive([]);
const currentAccount = ref({});
const targetAccount = ref({});
const transaction = reactive({
  notes: ''
});
const categories = ref([]);
let filteredCategories = ref([]);

const itemType = ref('expense');
transaction.is_transfer = itemType.value === 'transfer';

function changeAccount({ accountType, account }) {
  if (accountType==='src') {
    currentAccount.value = account;
  } else {
    targetAccount.value = account;
  }
}

onBeforeMount(async () => {
  try {
    accounts.length = 0;
    accounts.push(...(await accountService.getAllUserAccounts()));
    currentAccount.value = accounts[0];
    targetAccount.value = accounts[0];
    transaction.account_id = currentAccount.value.id;
    transaction.target_account_id = targetAccount.value.id;
    categories.value = await categoriesService.getUserCategories();
    filterCategories();
  } catch (e) {
    console.log(e.message);
    router.push({ name: 'login' });
  }
});

function filterCategories() {
  const isIncome = itemType.value === 'income';
  filteredCategories.value = categories.value.filter((item) => item.is_income === isIncome);
  updateTransactionProperties(itemType.value);
}

function updateTransactionProperties(type) {
  if (type === 'transfer') {
    transaction.category_id = null;
    transaction.is_transfer = true;
    transaction.target_account_id = targetAccount.value.id;
  } else {
    transaction.target_account_id = null;
    transaction.is_transfer = false;
    transaction.category_id = filteredCategories.value[0].id;
  }
}

function changeNotes($event) {
  transaction.notes = $event.target.value;
}

function changeItemType(type) {
  itemType.value = type;
  filterCategories();
  updateTransactionProperties(type);
}

function submitNewTransaction() {
  transactionsService.addTransaction(transaction);
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <form @submit.prevent="submitNewTransaction">
            <TransactionTypeTabs @type-changed="changeItemType" :transaction="transaction" :item-type="itemType" />

            <TransactionLabel :transaction="transaction" />

            <TransactionAmount :transaction="transaction" :current-account="currentAccount" />

            <Category v-if="!transaction.is_transfer" :item-type="itemType" :transaction="transaction"
              :categories="filteredCategories" />

            <Account :transaction="transaction" @account-changed="changeAccount" account-type="src"
              :accounts="accounts" />

            <Account v-if="transaction.is_transfer === true" account-type="target" :transaction="transaction"
              :accounts="accounts" />

            <div class="mb-3">
              <label for="notes" class="form-label">Notes</label>
              <textarea @keyup="changeNotes" class="form-control" id="notes"
                rows="3">{{ transaction?.notes }}</textarea>
            </div>

            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>
