<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps(['transaction', 'accounts', 'accountType']);
const emit = defineEmits(['accountChanged']);

const t = useI18n().t;

function changeAccount($event) {
  const acc = props.accounts[$event.target.value];
  const accountId = acc.id;
  if (props.accountType === 'src') {
    props.transaction.accountId = accountId;
  } else {
    props.transaction.targetAccountId = accountId;
  }
  emit('accountChanged', {
    accountType: props.accountType,
    account: acc
  });
}

const accountIdx = computed(() => {
  if (props.accountType === 'src') {
    // console.log(props.transaction.accountId);
    // console.log(props.accounts);
    // console.log(props.accounts.findIndex((item) => item.id === props.transaction.accountId));
    return props.accounts.findIndex((item) => item.id === props.transaction.accountId);
  } else {
    return props.accounts.findIndex((item) => item.id === props.transaction.targetAccountId);
  }
});

const accLabel = computed(() => {
  if (props.accountType === 'src') {
    return t('message.account');
  } else {
    return t('message.targetAccount');
  }
});
</script>

<template>
  <label for="label" class="form-label">
    {{ accLabel }}
  </label>
  <select class="form-select bottom-space" @change="changeAccount" :value="accountIdx">
    <option v-for="(acc, index) in accounts" :key="acc.id" :value="index">
      {{ acc.name }} ({{ acc.balance }} {{ acc.currency.code }})
    </option>
  </select>
</template>
