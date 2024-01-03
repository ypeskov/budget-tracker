<script setup>
import { DateTime } from 'luxon';
import { computed } from 'vue';

const props = defineProps(['transactions',]);

function categoryLabel(transaction) {
  if (transaction.category) {
    return `${transaction.category.name} (${transaction.isIncome ? 'Income' : 'Expense'})`;
  } else if (transaction.is_transfer) {
    return 'Transfer';
  } else {
    return 'Unknown';
  }
}

</script>

<template>
  <div v-if="transactions.length > 0">
    <div v-for="transaction, idx in props.transactions" :key="transaction.id" class="list-item">
      <RouterLink class="row" :to="{
        name: 'transactionDetails',
        params: {
          id: transaction.id,
        }
      }">
        <div class="col-5">
          <div class="transaction-element"><b>{{ transaction.label }}</b></div>
          <div class="transaction-element">{{ categoryLabel(transaction) }}</div>

        </div>
        <div class="col-7 amount-container">
          <div><b>{{ parseFloat(transaction.amount).toFixed(2) }} {{ transaction.currency.code }}</b></div>
          <div><span class="acc-name">{{ transaction.account.name }}</span> | {{
            parseFloat(transaction.newBalance).toFixed(2) }}</div>
        </div>
      </RouterLink>
    </div>
  </div>
  <div v-else>
    No transactions found
  </div>
</template>

<style scoped>
@import '../../assets/main.scss';

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
</style>