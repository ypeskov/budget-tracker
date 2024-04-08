<script setup>
import { computed, onBeforeMount, reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import { RouterLink, useRouter } from 'vue-router';

import { Services } from '../../services/servicesConfig';
import { processError } from '../../errors/errorHandlers';

const props = defineProps(['transactions', 'accountId', 'returnUrl']);

const router = useRouter();
const t = useI18n().t;

const categories = reactive([]);

onBeforeMount(async () => {
  categories.length = 0;
  try {
    const tmpCategories = await Services.categoriesService.getUserCategories();
    if (tmpCategories) {
      categories.push(...tmpCategories);
    }
  } catch (e) {
    await processError(e, router);
  }
});

const groupedTransactions = computed(() => {
  const grouped = [];
  let lastDate = null;

  props.transactions.forEach(transaction => {
    const transactionDate = transaction.dateTime.split('T')[0];
    if (lastDate !== transactionDate) {
      grouped.push({ date: transactionDate, transactions: [] });
      lastDate = transactionDate;
    }
    grouped[grouped.length - 1].transactions.push(transaction);
  });

  return grouped;
});

const getParentCategoryLabel = (transaction) => {
  if (transaction.category) {
    const parentCategory = categories.find(category => category.id === transaction.category.parentId);
    return parentCategory ? `[${parentCategory.name}] : ` : '';
  }
  return '';
};

const categoryLabel = transaction => transaction.category?.name || (transaction.isTransfer ? 'Transfer' : 'Unknown');

const transactionClass = (transaction) => {
  if (transaction.isTransfer) {
    return 'transfer-transaction';
  } else if (transaction.isIncome) {
    return 'income-transaction';
  } else {
    return 'expense-transaction';
  }
};

function accountName(account) {
  if (account.isDeleted) {
    return `${account.name} (${t('message.deleted')})`;
  } else {
    return account.name;
  }
}
</script>

<template>
  <div v-if="groupedTransactions.length > 0">
    <div v-for="group in groupedTransactions" :key="group.date">
      <div class="date-header">{{ group.date }}</div>
      <div v-for="transaction in group.transactions" :key="transaction.id" class="list-item">
        <RouterLink class="row" :to="{
          name: 'transactionDetails',
          params: {
            id: transaction.id
          },
          query: {
            returnUrl: props.returnUrl,
            accountId: props.accountId,
          }
        }">
          <div class="col-5">
            <div class="transaction-element"><b>{{ transaction.label }}</b></div>
            <div class="transaction-element"
            ><b>{{ getParentCategoryLabel(transaction) }}</b>{{ categoryLabel(transaction) }}</div>
          </div>
          <div class="col-7 amount-container">
            <div>
              <b :class="transactionClass(transaction)"
              >{{ $n(transaction.amount, 'decimal') }}{{ transaction.currency.code }}</b>
            </div>
            <div>
              <span class="acc-name">{{ accountName(transaction.account) }}</span>
              | {{ $n(transaction.newBalance, 'decimal') }}
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
  <div v-else>
    No transactions found
  </div>
</template>

<style scoped>
@import '../../assets/main.scss';

.date-header {
  font-weight: bold;
  margin: 10px 0;
  background-color: #b3b2b2;
  padding: 5px;
  border-radius: 5px;
}

.list-item {
  padding: 5px;
  border: 1px solid #eee;
  border-radius: 5px;
  margin-top: 5px;
}

.transaction-element {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.amount-container {
  text-align: right;
}

.acc-name {
  color: blue;
}

.transfer-transaction {
}

.income-transaction {
  color: green;
}

.expense-transaction {
  color: red;
}
</style>
