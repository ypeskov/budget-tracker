<script setup>
import { RouterLink } from 'vue-router';
const props = defineProps(['accounts', 'totalBalance', 'baseCurrencyCode']);

function balanceClass(balance) {
  return balance < 0 ? 'text-danger' : 'text-success';
}

function availableBalanceCC(acc) {
  return acc.balance + acc.creditLimit;
}
</script>

<template>
  <div class="row">
    <div class="col">
      <div>
        <b>{{ $t('message.yourAccounts') }}</b>
        ( {{ $t('message.totalBalance') }}: {{ $n(totalBalance, 'decimal') }} {{ baseCurrencyCode }})
      </div>
    </div>
  </div>
  <div v-for="acc in props.accounts" :key="acc.id" class="list-item">
    <RouterLink class="account-link" :to="{name: 'accountDetails', params: {id: acc.id}}">
      <div class="row account-item">
        <div class="col-4 account-name">
          {{ acc.name }}
        </div>
        <div class="col account-balance" :class="balanceClass(acc.balance)">
          <div>
            <b>{{ $n(acc.balance, 'decimal') }}</b>
            <span v-if="acc.accountTypeId===4"> ({{ $n(availableBalanceCC(acc), 'decimal') }})</span>
            {{ acc.currency.code }}
          </div>
          <div v-if="baseCurrencyCode !== acc.currency.code">
            ({{ $n(acc.balanceInBaseCurrency, 'decimal') }} {{ baseCurrencyCode }})
          </div>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/main.scss' as *;

.account-name {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  -webkit-line-clamp: 3;
  max-height: calc(3 * 1.2em);
  line-height: 1.2;
}

.account-balance {
  text-align: right;
}

.list-item > a {
  text-decoration: none;
  color: black;
}

.account-marks {
  text-align: right;
}
</style>