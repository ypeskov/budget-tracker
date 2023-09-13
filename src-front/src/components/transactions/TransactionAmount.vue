<script setup>
const props = defineProps(['transaction', 'currentAccount']);
props.transaction.amount = 0;
</script>

<template>
  <div class="mb-3">
    <div class="row">
      <div class="col-10">
        <label for="amount" class="form-label">
          Amount
        </label>
        <input type="number" v-model="transaction.amount" class="form-control" id="amount" />
      </div>
      <div class="col-2 currency">{{ currentAccount?.currency?.code }}</div>
    </div>
  </div>
</template>

<style scoped>
.currency {
  align-self: flex-end;
}
</style>
