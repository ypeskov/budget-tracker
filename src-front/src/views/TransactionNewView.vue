<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';

import { Services } from '../services/servicesConfig';

import TransactionTypeTabs from '../components/transactions/TransactionTypeTabs.vue';
import TransactionLabel from '../components/transactions/TransactionLabel.vue';
import TransactionAmount from '../components/transactions/TransactionAmount.vue';
import Category from '../components/transactions/Category.vue';
import Account from '../components/transactions/Account.vue';
import ExchangeRate from '../components/transactions/ExchangeRate.vue';

const props = defineProps(['isEdit', 'returnUrl', 'accountId']);
const router = useRouter();
const route = useRoute();
const { t } = useI18n();

const accounts = reactive([]);
const currentAccount = ref(accounts[0]);
const targetAccount = ref(accounts[0]);
let transaction = reactive({});
const categories = ref([]);
let filteredCategories = ref([]);
const showDeleteConfirmation = ref(false);

const itemType = ref('expense');
transaction.is_transfer = itemType.value === 'transfer';

const returnUrlName = ref('');

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
  if (props.returnUrl === 'accountDetails') {
    returnUrlName.value = 'accountDetails';
  } else {
    returnUrlName.value = 'transactions';
  }

  try {
    accounts.length = 0;
    accounts.push(...(await Services.accountsService.getAllUserAccounts()));
    currentAccount.value = accounts[0];
    targetAccount.value = accounts[0];
    transaction.account_id = currentAccount.value.id;
    transaction.target_account_id = targetAccount.value.id;
    categories.value = await Services.categoriesService.getUserCategories();

    if (props.isEdit) {
      const details = await Services.transactionsService.getTransactionDetails(route.params.id);
      transaction = Object.assign(transaction, details);
      itemType.value = transaction.is_transfer ? 'transfer' : transaction.is_income ? 'income' : 'expense';
      currentAccount.value = accounts.find((item) => item.id === transaction.account_id);
      targetAccount.value = accounts.find((item) => item.id === transaction.target_account_id);
      if (targetAccount.value === undefined) {
        targetAccount.value = accounts[0];
      }
    }

    filterCategories();
  } catch (e) {
    console.log(e);
    await router.push({ name: 'home' });
  }
});

function filterCategories() {
  const isIncome = itemType.value === 'income';
  // filter categories by income/expense
  filteredCategories.value = categories.value.filter((item) => item.is_income === isIncome);

  // if the current category is not in the filtered categories, set the first one from the filtered list
  if (!filteredCategories.value.some((item) => item.id === transaction.category_id)) {
    transaction.category_id = filteredCategories.value[0].id;
  }

  updateTransactionProperties(itemType.value);
}

function updateTransactionProperties(type) {
  if (type === 'transfer') {
    transaction.category_id = transaction.category_id || null;
    transaction.is_transfer = true;
    transaction.target_account_id = targetAccount.value.id;
    transaction.is_income = false;
  } else {
    transaction.target_account_id = null;
    transaction.is_transfer = false;
    transaction.category_id = transaction.category_id || filteredCategories.value[0].id;
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

async function submitTransaction() {
  try {
    if (props.isEdit) {
      console.log(transaction);
      await Services.transactionsService.updateTransaction(transaction);
    } else {
      await Services.transactionsService.addTransaction(transaction);
    }
    for (const key in transaction) {
      transaction[key] = null;
    }
    await router.push({
      name: returnUrlName.value,
      params: {
        id: props.accountId,
      },
    });
    // router.go(-1);
  } catch (e) {
    console.log(e);
    await router.push({ name: 'home' });
  }
}

function confirmDelete() {
  showDeleteConfirmation.value = true;
}

async function deleteTransaction() {
  try {
    await Services.transactionsService.deleteTransaction(transaction.id);
    await router.push({ name: 'transactions' });
  } catch (e) {
    console.log(e);
    await router.push({ name: 'home' });
  } finally {
    showDeleteConfirmation.value = false;
  }
}
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col">
          <form @submit.prevent="submitTransaction">
            <TransactionTypeTabs @type-changed="changeItemType" :transaction="transaction" :item-type="itemType" />

            <TransactionLabel :transaction="transaction" />

            <Account :transaction="transaction" @account-changed="changeAccount" account-type="src"
                     :accounts="accounts" />

            <TransactionAmount :label="t('message.amount')" type="src"
                               :transaction="transaction" @amount-changed="amountChanged"
                               :current-account="currentAccount" />

            <Account v-if="transaction.is_transfer === true" @account-changed="changeAccount" account-type="target"
                     :transaction="transaction" :accounts="accounts" />

            <TransactionAmount v-if="itemType === 'transfer'" type="target" :label="t('message.amount')"
                               @amount-changed="amountChanged" :transaction="transaction"
                               :current-account="targetAccount" />

            <ExchangeRate v-if="itemType === 'transfer'" :amount-src="transaction.amount"
                          :currency-src="currentAccount.currency.code" :currency-target="targetAccount.currency.code"
                          :target-amount="transaction.target_amount" />

            <Category v-if="!transaction.is_transfer"
                      :transaction="transaction"
                      :categories="filteredCategories"
                      @update:categoryId="transaction.categoryId = $event" />

            <div class="mb-3">
              <label for="notes" class="form-label">{{ $t('message.notes') }}</label>
              <textarea @keyup="changeNotes" class="form-control" id="notes" v-model="transaction.notes"
                        rows="3"></textarea>
            </div>

            <div class="flex-container">
              <button type="submit" class="btn btn-primary">{{ $t('buttons.submit') }}</button>
              <button @click.prevent="confirmDelete" class="btn btn-danger">{{ $t('buttons.delete') }}</button>
            </div>
          </form>

          <div v-if="showDeleteConfirmation" class="overlay"></div>

          <div v-if="showDeleteConfirmation" class="delete-confirmation">
            <p>Delete the transaction?</p>
            <div class="buttons-container">
              <button @click="deleteTransaction" class="btn btn-danger">{{ $t('buttons.yes') }}</button>
              <button @click="showDeleteConfirmation = false"
                      class="btn btn-secondary">{{ $t('buttons.cancel') }}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.flex-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.delete-confirmation {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  text-align: center;
  width: auto;
}

.delete-confirmation p {
  margin-bottom: 20px;
  font-size: 16px;
  color: #333;
}

.buttons-container {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}
</style>