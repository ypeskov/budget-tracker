<script setup>
import { computed, onBeforeMount } from 'vue';

const props = defineProps(['transaction', 'accounts', 'accountType']);
const emit = defineEmits(['accountChanged']);

function changeAccount($event) {
  const acc = props.accounts[$event.target.value];
  const accountId = acc.id;
  if (props.accountType === 'src') {
    props.transaction.account_id = accountId;
  } else {
    props.transaction.target_account_id = accountId;
  }
  emit('accountChanged', {
    accountType: props.accountType,
    account: acc
  });
}

const accLabel = computed(() => {
  if (props.accountType === 'src') {
    return 'Account';
  } else {
    return 'Target Account';
  }
});
</script>

<template>
  <label for="label" class="form-label">
    {{ accLabel }}
  </label>
  <select class="form-select bottom-space" @change="changeAccount">
    <option v-for="(acc, index) in accounts" :key="acc.id" :value="index">
      {{ acc.name }} ({{ acc.balance }} {{ acc.currency.code }})
    </option>
  </select>
</template>
