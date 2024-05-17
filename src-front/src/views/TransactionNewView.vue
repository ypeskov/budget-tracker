<script setup>
import { onBeforeMount, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { DateTime } from 'luxon';

import { Services } from '../services/servicesConfig';
import { processError } from '../errors/errorHandlers';

import TransactionTypeTabs from '../components/transactions/TransactionTypeTabs.vue';
import TransactionLabel from '../components/transactions/TransactionLabel.vue';
import TransactionAmount from '../components/transactions/TransactionAmount.vue';
import Category from '../components/transactions/Category.vue';
import AccountSelector from '../components/transactions/AccountSelector.vue';
import ExchangeRate from '../components/transactions/ExchangeRate.vue';
import TransactionDateTime from '../components/transactions/TransactionDateTIme.vue';

const props = defineProps(['isEdit', 'returnUrl', 'accountId']);
const router = useRouter();
const route = useRoute();
const { t } = useI18n();

const accounts = reactive([]);
const currentAccount = ref(accounts[0]);
const targetAccount = ref(accounts[0]);
const categories = ref([]);
const showDeleteConfirmation = ref(false);

const srcAccountId = ref(null);
const targetAccountId = ref(null);
const srcAmount = ref(null);
const targetAmount = ref(null);

let targetTransaction = reactive({});
let transaction = reactive({});
let filteredCategories = ref([]);

const itemType = ref('expense');
transaction.isTransfer = itemType.value === 'transfer';

const returnUrlName = ref('');

function changeAccount({ accountType, accountId }) {
  console.log(srcAccountId.value, targetAccountId.value, {...transaction});
  if (accountType === 'src') {
    srcAccountId.value = accountId;
  } else if (accountType === 'target') {
    targetAccountId.value = accountId;
  }
  console.log('-------------------')
  console.log(srcAccountId.value, targetAccountId.value, {...transaction});
  if (targetAccountId.value === transaction.accountId || srcAccountId.value === transaction.targetAccountId) {
    transaction.isIncome = !transaction.isIncome;
  }
}

function amountChanged({ amountType, amount }) {
  if (transaction.isTransfer) {
    if (amountType === 'src') {
      srcAmount.value = amount;
    } else {
      targetAmount.value = amount;
    }
  } else {
    srcAmount.value = amount;
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
    accounts.push(...(await Services.accountsService.getUserAccounts()));
    if (props.accountId) {
      currentAccount.value = accounts.find((item) => item.id === parseInt(props.accountId, 10));
    } else {
      currentAccount.value = accounts[0];
    }
    srcAccountId.value = currentAccount.value.id;

    targetAccount.value = accounts[0];

    categories.value = await Services.categoriesService.getUserCategories();

    if (props.isEdit) {
      const details = await Services.transactionsService.getTransactionDetails(route.params.id);
      transaction = Object.assign(transaction, details);
      itemType.value = transaction.isTransfer ? 'transfer' : transaction.isIncome ? 'income' : 'expense';
      srcAccountId.value = transaction.accountId;
      srcAmount.value = transaction.amount;
      currentAccount.value = accounts.find((item) => item.id === srcAccountId.value);

      if (transaction.linkedTransactionId) {
        await getLinkedTransaction(transaction);
      }
    }

    filterCategories();
  } catch (e) {
    await processError(e, router);
  }
});

async function getLinkedTransaction(transaction) {
  const linkedTransaction = await Services.transactionsService.getTransactionDetails(transaction.linkedTransactionId);
  targetTransaction = Object.assign(targetTransaction, linkedTransaction);

  if (transaction.isTransfer) {
    if (transaction.isIncome === false) {
      targetAccountId.value = linkedTransaction.accountId;
      targetAmount.value = linkedTransaction.amount;
    } else {
      srcAccountId.value = linkedTransaction.accountId;
      targetAccountId.value = transaction.accountId;
      targetAmount.value = transaction.amount;
      srcAmount.value = linkedTransaction.amount;
    }
  }
}

function filterCategories() {
  const isIncome = itemType.value === 'income';
  // filter categories by income/expense
  filteredCategories.value = categories.value.filter((item) => item.isIncome === isIncome);

  // if the current category is not in the filtered categories, set the first one from the filtered list
  if (!filteredCategories.value.some((item) => item.id === transaction.categoryId)) {
    transaction.categoryId = filteredCategories.value[0].id;
  }

  updateTransactionProperties(itemType.value);
}

function updateTransactionProperties(type) {
  if (type === 'transfer') {
    transaction.categoryId = null;
    transaction.isTransfer = true;
  } else {
    transaction.targetAccountId = null;
    targetAmount.value = null;
    transaction.isTransfer = false;
    transaction.categoryId = transaction.categoryId || filteredCategories.value[0].id;
    transaction.isIncome = itemType.value === 'income';
  }
}

function changeNotes($event) {
  transaction.notes = $event.target.value;
}

function changeItemType(type) {
  itemType.value = type;
  filterCategories();
}

function dateTimeChanged({ date, time }) {
  const dateTimeString = `${date}T${time}`;
  const localDateTime = DateTime.fromISO(dateTimeString, { zone: 'local' });
  transaction.dateTime = localDateTime.toUTC().toISO().replace('.000', '');
}

async function submitTransaction() {
  transaction.accountId = srcAccountId.value;
  transaction.amount = srcAmount.value;
  transaction.targetAccountId = targetAccountId.value;
  transaction.targetAmount = targetAmount.value;

  try {
    if (props.isEdit) {
      console.log('transaction', {...transaction});
      await Services.transactionsService.updateTransaction(transaction);
    } else {
      await Services.transactionsService.addTransaction(transaction);
    }
    await router.push({
      name: returnUrlName.value,
      params: {
        id: props.accountId,
      },
    });
  } catch (e) {
    await processError(e, router);
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
    await processError(e, router);
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
            <TransactionTypeTabs @type-changed="changeItemType"
                                 :is-edit="props.isEdit"
                                 :transaction="transaction"
                                 :item-type="itemType" />

            <TransactionLabel :transaction="transaction" />

            <AccountSelector @account-changed="changeAccount"
                             :label="$t('message.account')"
                             account-type="src"
                             :accountId="srcAccountId"
                             :accounts="accounts" />

            <TransactionAmount :label="t('message.amount')"
                               type="src"
                               @amount-changed="amountChanged"
                               :amount="srcAmount"
                               :current-account="currentAccount" />

            <AccountSelector v-if="itemType === 'transfer'"
                             @account-changed="changeAccount"
                             :label="$t('message.targetAccount')"
                             account-type="target"
                             :accountId="targetAccountId"
                             :accounts="accounts" />

            <TransactionAmount v-if="itemType === 'transfer'"
                               type="target"
                               :label="t('message.amount')"
                               @amount-changed="amountChanged"
                               :amount="targetAmount"
                               :current-account="targetAccount" />

            <ExchangeRate v-if="itemType === 'transfer'"
                          :currency-src-code="currentAccount.currency.code"
                          :src-amount="transaction.amount"
                          :currency-target-code="targetAccount.currency.code"
                          :target-amount="targetTransaction.amount" />

            <Category v-if="!transaction.isTransfer"
                      :transaction="transaction"
                      :categories="filteredCategories"
                      @update:categoryId="transaction.categoryId = $event" />

            <TransactionDateTime :transaction="transaction" :is-edit="isEdit" @date-time-changed="dateTimeChanged" />

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
                      class="btn btn-secondary">{{ $t('buttons.cancel') }}
              </button>
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