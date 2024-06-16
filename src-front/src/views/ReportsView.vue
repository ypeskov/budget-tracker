<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <main>
    <div class="container">
      <div class="row">
        <RouterLink :to="{ name: 'reports-cashflow' }">
          <button class="btn btn-secondary">{{ $t('buttons.cashFlowReport')}}</button>
        </RouterLink>
      </div>

      <div class="row">
        <RouterLink :to="{ name: 'reports-balance' }">
          <button class="btn btn-secondary">{{ $t('buttons.balanceReport')}}</button>
        </RouterLink>
      </div>

      <div class="row">
        <RouterLink :to="{ name: 'reports-expenses' }">
          <button class="btn btn-secondary">{{ $t('buttons.expensesReport')}}</button>
        </RouterLink>
      </div>
    </div>

  </main>
</template>

<style scoped>
button {
  width: 100%;
}
.row {
  margin: 1rem 1rem;
}
</style>