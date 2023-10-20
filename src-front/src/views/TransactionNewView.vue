<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

import { Services } from '../services/servicesConfig';

import TransactionTypeTabs from '../components/transactions/TransactionTypeTabs.vue';
import TransactionLabel from '../components/transactions/TransactionLabel.vue';
import TransactionAmount from '../components/transactions/TransactionAmount.vue';
import Category from '../components/transactions/Category.vue';
import Account from '../components/transactions/Account.vue';
import ExchangeRate from '../components/transactions/ExchangeRate.vue'

const router = useRouter();

const accounts = reactive([]);
const currentAccount = ref(accounts[0]);
const targetAccount = ref(accounts[0]);
const transaction = reactive({});
const categories = ref([]);
let filteredCategories = ref([]);

const itemType = ref('expense');
transaction.is_transfer = itemType.value === 'transfer';

function changeAccount({ accountType, account }) {
  if (accountType === 'src') {
    currentAccount.value = account;
  } else if (accountType === 'target') {
    targetAccount.value = account;
  }
}

function amountChanged({ amountType, amount }) {
  if (amountType === 'src') {
    transaction.amount = amount;
  } else {
    transaction.target_amount = amount;
  }
}

onBeforeMount(async () => {
  try {
    accounts.length = 0;
    accounts.push(...(await Services.accountsService.getAllUserAccounts()));
    currentAccount.value = accounts[0];
    targetAccount.value = accounts[0];
    transaction.account_id = currentAccount.value.id;
    transaction.target_account_id = targetAccount.value.id;
    categories.value = await Services.categoriesService.getUserCategories();
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
    transaction.is_income = false;
  } else {
    transaction.target_account_id = null;
    transaction.is_transfer = false;
    transaction.category_id = filteredCategories.value[0].id;
    transaction.is_income = itemType.value === 'income';
  }
}

function changeNotes($event) {
  transaction.notes = $event.target.value;
}

function changeItemType(type) {
  itemType.value = type;
  filterCategories();
}

async function submitNewTransaction() {
  await Services.transactionsService.addTransaction(transaction);
  for (const key in transaction) {
    transaction[key] = null;
  }
  router.push({ name: 'transactions' });
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

            <Account :transaction="transaction" @account-changed="changeAccount" account-type="src"
              :accounts="accounts" />

            <TransactionAmount label="Amount" type="src" :transaction="transaction" @amount-changed="amountChanged"
              :current-account="currentAccount" />

            <Account v-if="transaction.is_transfer === true" @account-changed="changeAccount" account-type="target"
              :transaction="transaction" :accounts="accounts" />

            <TransactionAmount v-if="itemType === 'transfer'" type="target" label="Target Amount"
              @amount-changed="amountChanged" :transaction="transaction" :current-account="targetAccount" />

            <ExchangeRate v-if="itemType === 'transfer'" :amount-src="transaction.amount"
              :currency-src="currentAccount.currency.code" :currency-target="targetAccount.currency.code"
              :target-amount="transaction.target_amount" />

            <Category v-if="!transaction.is_transfer" :item-type="itemType" :transaction="transaction"
              :categories="filteredCategories" />

            <div class="mb-3">
              <label for="notes" class="form-label">Notes</label>
              <textarea @keyup="changeNotes" class="form-control" id="notes" v-model="transaction.notes"
                rows="3"></textarea>
            </div>

            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>
