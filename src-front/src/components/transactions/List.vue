<script setup>
import { DateTime } from 'luxon';

const props = defineProps(['transactions',]);
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
        <div class="col-7">
          <div class="transaction-element"><b>{{ transaction.label }}</b></div>
          <div class="transaction-element">{{ transaction.notes }}</div>
        </div>
        <div class="col-5 amount-container">
          <div><b>{{ parseFloat(transaction.amount).toFixed(2) }} {{ transaction.currency.code }}</b></div>
          <div>{{ DateTime.fromISO(transaction.date_time).toLocaleString() }}</div>
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
</style>