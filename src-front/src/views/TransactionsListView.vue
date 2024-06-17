<script setup>
import ListContainer from '../components/transactions/ListContainer.vue';

const props = defineProps(['accountId', 'isAccountDetails', 'categories']);

</script>

<template>
  <main>
    <ListContainer :account-id="props.accountId"
                   :initial-categories="props.categories"
                   :is-account-details="!!props.isAccountDetails" />
  </main>
</template>

<style scoped  lang="scss">
@import '../assets/main.scss';

.transaction-element {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.amount-container {
  text-align: right;
}

.active-filter {
  font-weight: bold;
  color: #ffffff;
}
</style>