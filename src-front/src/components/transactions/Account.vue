<script setup>
import { computed, onBeforeMount, ref } from 'vue';

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
    acountType: props.accountType,
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

onBeforeMount(() => { });
</script>

<template>
  <label for="label" class="form-label">
    {{ accLabel }}
  </label>
  <select class="form-select bottom-space" @change="changeAccount">
    <option v-for="(acc, index) in accounts" :key="acc.id" :value="index">
      {{ acc.name }}
    </option>
  </select>
</template>
